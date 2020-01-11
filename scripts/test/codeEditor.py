#!/usr/bin/python3
# QcodeEditor.py by acbetter.
# -*- coding: utf-8 -*-

# NOTE https://stackoverflow.com/questions/40386194/create-text-area-textedit-with-line-number-in-pyqt
import os
import re
import sys
import keyword

from maya import cmds
from maya import OpenMayaUI

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QRect, QSize,QRegExp
from PySide2.QtWidgets import QWidget, QPlainTextEdit, QTextEdit,QVBoxLayout
from PySide2.QtGui import QColor, QPainter, QTextFormat,QTextCharFormat,QFont,QSyntaxHighlighter

from Qt.QtCompat import wrapInstance

# from PySide2.QtGui import *
# from PySide2.QtCore import *
# from PySide2.QtWidgets import *
LINEBAR_COLOR = QColor("#444444")
LINE_COLOR = QColor("dark")
class Highlighter(QSyntaxHighlighter):
    """syntax highlighter"""
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        self.__rules = []
        
        # numeric color
        self._numericFormat = QTextCharFormat()
        self._numericFormat.setForeground(QColor('#9ACD32'))
        
        # mel command options started with -
        melOpsFormat = QTextCharFormat()
        melOpsFormat.setForeground(QColor('#B8860B'))
        self.__rules.append((re.compile('-[a-zA-Z]+\\b'), melOpsFormat))

        # keywords color
        self._keywordColor = QColor(0, 128, 255)

        self._numeric()
        self._keywordFormat()
        self._cmdsFunctionFormat()

        # maya api format
        mapiFormat = QTextCharFormat()
        mapiFormat.setForeground(self._keywordColor)
        self.__rules.append((re.compile('\\bM\\w+\\b'), mapiFormat))
        # Qt
        self.__rules.append((re.compile('\\bQ\\w+\\b'), mapiFormat))

        # quotation
        self._quotationFormat = QTextCharFormat()
        self._quotationFormat.setForeground(Qt.green)
        # quote: ""
        self.__rules.append((re.compile('".*"'), self._quotationFormat))
        # single quotes for python: ''
        self.__rules.append((re.compile("'.*'"), self._quotationFormat))

        # sing line comment
        self._commentFormat = QTextCharFormat()
        # orange red
        self._commentFormat.setForeground(QColor(255, 128, 64))
        # // mel comment
        self.__rules.append((re.compile('//[^\n]*'), self._commentFormat))
        # # python comment
        self.__rules.append((re.compile('#[^\n]*'), self._commentFormat))

        # function and class format
        funcFormat = QTextCharFormat()
        funcFormat.setFontWeight(QFont.Bold)
        self.__rules.append((re.compile('\\b(\\w+)\(.*\):'), funcFormat))

        # mel warning
        warningFormat = QTextCharFormat()
        warningFormat.setForeground(QColor('#FF9ACD32'))
        warningFormat.setBackground(Qt.yellow)
        warningFormat.setFontWeight(QFont.Bold)
        self.__rules.append((re.compile('// Warning:[^\n]*//'), warningFormat))

        # mel error
        errorFormat = QTextCharFormat()
        errorFormat.setForeground(QColor('#FF9ACD32'))
        errorFormat.setBackground(Qt.red)
        errorFormat.setFontWeight(QFont.Bold)
        self.__rules.append((re.compile('// Error:[^\n]*//'), errorFormat))

        # Quotes
        self._singleQuotes = QRegExp("'''")
        self._doubleQuotes = QRegExp('"""')

        # mel multi-line comment: /*  */
        self._melMLComStart = re.compile('/\\*')
        self._melMLComEnd = re.compile('\\*/')
        
    def _numeric(self):
        '''set up numeric format'''
        num_01 = re.compile('\\b[+-]?[0-9]+[lL]?\\b')
        num_02 = re.compile('\\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\\b')
        num_03 = re.compile('\\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\\b')
        num_regs = (num_01, num_02, num_03)
        for nr in num_regs:
            self.__rules.append((nr, self._numericFormat))

    def _keywordFormat(self):
        '''set up keyword format'''
        # mel keyword
        melKeywords = ['false', 'float', 'int', 'matrix', 'off', 'on', 'string',
                       'true', 'vector', 'yes', 'alias', 'case', 'catch', 'break',
                       'case', 'continue', 'default', 'do', 'else', 'for', 'if', 'in',
                       'while', 'alias', 'case', 'catch', 'global', 'proc', 'return', 'source', 'switch']
        # python keyword
        pyKeywords = keyword.kwlist + ['False', 'True', 'None']

        keywords = {}.fromkeys(melKeywords)
        keywords.update({}.fromkeys(pyKeywords))
        # keyword format
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(self._keywordColor)
        keywordFormat.setFontWeight(QFont.Bold)
        kwtext = '\\b(' + "|".join(keywords) + ')\\b'
        self.__rules.append((re.compile(kwtext), keywordFormat))

    def _cmdsFunctionFormat(self):
        '''set up maya.cmds functions'''
        mayaBinDir = os.path.dirname(sys.executable)
        cmdsList = os.path.join(mayaBinDir, 'commandList')
        functions = '\\b('
        with open(cmdsList) as phile:
            for line in phile:
                functions += line.split(' ')[0] + '|'

        # global MEL procedures
        melProcedures = cmds.melInfo()
        maxlen = 1400
        stop = len(melProcedures) / maxlen
        melProc = []
        melProc.append('\\b(' + '|'.join(melProcedures[:maxlen]) + ')\\b')
        for i in range(1, stop - 1):
            start = maxlen * i
            end = maxlen * (i + 1)
            melProc.append('\\b(' + '|'.join(melProcedures[start:end]) + ')\\b')
        melProc.append('\\b(' + '|'.join(melProcedures[maxlen*stop:]) + ')\\b')

        # TODO: should update it when a plug-in was load.
        # function from plug-ins
        plugins = cmds.pluginInfo(q=1, listPlugins=1)
        for plugin in plugins:
            funcFromPlugin = cmds.pluginInfo(plugin, q=1, command=1)
            if funcFromPlugin:
                functions += '|'.join(funcFromPlugin)
        functions = functions[:-1] + ')\\b'

        # function format
        funcFormat = QTextCharFormat()
        funcFormat.setForeground(self._keywordColor)
        self.__rules.append((re.compile(functions), funcFormat))
        for mp in melProc:
            self.__rules.append((re.compile(mp), funcFormat))

    def _melMLCommentFormat(self, text):
        '''set up mel multi-line comment: /*  */'''
        startIndex = 0
        commentLen = 0
        self.setCurrentBlockState(0)
        if self.previousBlockState() != 1:
            searchStart = self._melMLComStart.search(text)
            if searchStart:
                startIndex = searchStart.start()
                searchEnd = self._melMLComEnd.search(text)
                if searchEnd:
                    commentLen = searchEnd.end() - startIndex
                else:
                    self.setCurrentBlockState(1)
                    commentLen = len(text) - startIndex
        else:
            searchEnd = self._melMLComEnd.search(text)
            if searchEnd:
                commentLen = searchEnd.end()
            else:
                self.setCurrentBlockState(1)
                commentLen = len(text)
        if commentLen > 0:
            self.setFormat(startIndex, commentLen, self._commentFormat)
            
    def quotesFormat(self, text, regExp, state):
        '''set up single or double quotes strings format'''
        if self.previousBlockState() == state:
            startIndex = 0
            add = 0
        else:
            startIndex = regExp.indexIn(text)
            add = regExp.matchedLength()
            
        while startIndex >= 0:
            end = regExp.indexIn(text, startIndex + add)
            if end >= add:
                quotesLen = end - startIndex + regExp.matchedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(state)
                quotesLen = len(text) - startIndex + add
            self.setFormat(startIndex, quotesLen, self._quotationFormat)
            startIndex = regExp.indexIn(text, startIndex + quotesLen)
            
        if self.currentBlockState() == state:
            return True
        else:
            return False

    def highlightBlock(self, text):
        '''highlight text'''
        for regExp, tformat in self.__rules:
            match = regExp.search(text)
            while match:
                self.setFormat(match.start(), match.end() - match.start(), tformat)
                match = regExp.search(text, match.end())

        # blocks
        self._melMLCommentFormat(text)
        quotesState = self.quotesFormat(text, self._singleQuotes, 2)
        if not quotesState:
            self.quotesFormat(text, self._doubleQuotes, 3)


# class QLineNumberArea(QWidget):
#     def __init__(self, editor):
#         super().__init__(editor)
#         self.codeEditor = editor

#     def sizeHint(self):
#         return QSize(self.editor.lineNumberAreaWidth(), 0)

#     def paintEvent(self, event):
#         self.codeEditor.lineNumberAreaPaintEvent(event)

class QLineNumberArea(QWidget):
    def __init__(self, parent = None):
        super(QLineNumberArea, self).__init__(parent)
        self.fixWidth = 30

        self.editor = parent
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        self.update_width('1')


    def update_on_scroll(self, rect, scroll):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def update_width(self, string):
        width = self.fontMetrics().width(str(string)) + self.fixWidth
        if self.width() != width:
            self.setFixedWidth(width)

    def paintEvent(self, event):
        if self.isVisible():
            block = self.editor.firstVisibleBlock()
            height = self.fontMetrics().height()
            number = block.blockNumber()
            painter = QPainter(self)
            painter.fillRect(event.rect(), LINEBAR_COLOR)
            painter.drawRect(event.rect().width()-1, 0, event.rect().width(), event.rect().height() - 1)
            font = painter.font()

            current_block = self.editor.textCursor().block().blockNumber() + 1

            condition = True
            while block.isValid() and condition:
                block_geometry = self.editor.blockBoundingGeometry(block)
                offset = self.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()
                number += 1

                rect = QRect(0, block_top, self.width() - 5, height)

                if number == current_block:
                    font.setBold(True)
                    block_rect = QRect(5, block_top, self.width() - 10, height)
                    painter.fillRect(block_rect, Qt.red)
                else:
                    font.setBold(False)

                painter.setFont(font)
                painter.drawText(rect, Qt.AlignRight, '%i'%number)

                if block_top > event.rect().bottom():
                    condition = False

                block = block.next()

            painter.end()


class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super(QCodeEditor,self).__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(5)
        highlighter = Highlighter(parent=self)
        highlighter.setDocument(self.document())
        
        self.setStyleSheet('color:##c8c8c8')

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = self.lineNumberArea.fixWidth + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super(QCodeEditor,self).resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(LINE_COLOR).lighter(100)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def mayaShow(self,name=u"MPDB_DEBUGGER_UI"):
        # NOTE 如果变量存在 就检查窗口多开
        if cmds.window(name,q=1,ex=1):
            cmds.deleteUI(name)
        window = cmds.window(name,title=self.windowTitle())
        cmds.showWindow(window)
        # NOTE 将Maya窗口转换成 Qt 组件
        ptr = self.mayaToQT(window)
        ptr.setLayout(QtWidgets.QVBoxLayout())
        ptr.layout().setContentsMargins(0,0,0,0)
        ptr.layout().addWidget(self)

        ptr.setWindowTitle(self.windowTitle())
        ptr.setMaximumHeight(self.maximumHeight())
        ptr.setMaximumWidth(self.maximumWidth())

    def mayaToQT( self,name ):
        # Maya -> QWidget
        ptr = OpenMayaUI.MQtUtil.findControl( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findLayout( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
        if ptr is not None: return wrapInstance( long( ptr ), QtWidgets.QWidget )


if __name__ == '__main__':
    # import sys
    # from PySide2.QtWidgets import QApplication

    # app = QApplication(sys.argv)
    # codeEditor = QCodeEditor()
    # codeEditor.show()
    # sys.exit(app.exec_())

    codeEditor = QCodeEditor()
    codeEditor.mayaShow()