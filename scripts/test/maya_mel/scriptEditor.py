from maya import mel
from maya import cmds

global __scriptEditorExecuteAll
def __scriptEditorExecuteAll():
	executer = mel.eval("$temp = $gLastFocusedCommandExecuter")
	text = cmds.cmdScrollFieldExecuter(executer,q=1,text=1)
	exec(text)

global __scriptEditorExecute
def __scriptEditorExecute():
	executer = mel.eval("$temp = $gLastFocusedCommandExecuter")
	
	selected_text = cmds.cmdScrollFieldExecuter(executer,q=1,selectedText=1)
	if selected_text:
		exec(selected_text)
	else:
		text = cmds.cmdScrollFieldExecuter(executer,q=1,text=1)
		cmds.cmdScrollFieldExecuter(executer,e=1,clear=1)
		exec(text)


# NOTE 从 scriptEditorPanel.mel 复制下来的代码 | 修改 execute 按钮的执行代码 修复 Maya2017 运行崩溃问题
mel.eval('''
source "scriptEditorPanel.mel";

global proc int isFullPathToScriptFile(string $f, string $test)
{
	// In order to be a full path, we must have a directory.
	string $dir = dirname($f);
	return( size($dir) && `filetest $test $f` );
}


proc scriptEditorPredefines() 
//
// Predefinitions such as:
// Tagging for labels which are used multiple times.  We can call uiRes() for the specified
// labels later in the file.
//
{
	global string $gScriptEditorMenuBarPrefix = "scriptEditor";
	// Options Menu Item suffixes
	global string $showLineNumbersMenuItemSuffix = "ShowLineNumbersMenuItem";
	global string $useTabsForIndentMenuItemSuffix = "UseTabsForIndentMenuItem";
	global string $autoCloseBracesMenuItemSuffix = "AutoCloseBracesMenuItem";
	global string $commandCompletionMenuItemSuffix = "CommandCompletionMenuItem";
	global string $pathCompletionMenuItemSuffix = "PathCompletionMenuItem";
	global string $toolTipHelpMenuItemSuffix = "ToolTipHelpMenuItem";
	global string $showQuickHelpMenuItemSuffix = "QuickHelpMenuItem";
	global string $batchRenderMsgsMenuItemSuffix = "BatchRenderMessagesMenuItem";
	global string $echoAllCmdsMenuItemSuffix = "EchoAllCmdsMenuItem";
	global string $errorLineNumsMenuItemSuffix = "ErrorLineNumberMenuItem";
	global string $stackTraceMenuItemSuffix = "StackTraceMenuItem";
	global string $suppressResultsMenuItemSuffix = "SuppressResultsMenuItem";
	global string $suppressInfoMenuItemSuffix = "SuppressInfoMenuItem";
	global string $suppressWarningsMenuItemSuffix = "SuppressWarningsMenuItem";
	global string $suppressErrorsMenuItemSuffix = "SuppressErrorsMenuItem";
	global string $suppressErrorsMenuItemSuffix = "SuppressDupVarMessagesMenuItem";
	global string $suppressStackTraceMenuItemSuffix = "SuppressStackTraceMenuItem";
	global string $historyFilterNoneMenuItemSuffix = "FilterNoneMenuItem";
	global string $historyFilterMELMenuItemSuffix = "FilterMELMenuItem";
	global string $historyFilterPythonMenuItemSuffix = "FilterPythonMenuItem";
	global string $executerBackupFileName = "commandExecuter";
	global string $gLastUsedDir;
	
	// Tagging
	string $cancel					= (uiRes("m_scriptEditorPanel.kCancel"));
	// * menus
	string $file					= (uiRes("m_scriptEditorPanel.kFile"));
	string $edit					= (uiRes("m_scriptEditorPanel.kEdit"));
	string $history					= (uiRes("m_scriptEditorPanel.kHistory"));
	string $command					= (uiRes("m_scriptEditorPanel.kCommand"));
	string $help					= (uiRes("m_scriptEditorPanel.kHelp"));
	// file
	string $load					= (uiRes("m_scriptEditorPanel.kLoadScript"));
	string $source					= (uiRes("m_scriptEditorPanel.kSourceScript"));
	string $save					= (uiRes("m_scriptEditorPanel.kSaveScript"));
	string $saveToShelf				= (uiRes("m_scriptEditorPanel.kSaveScriptToShelf"));
	// edit
	string $undo					= (uiRes("m_scriptEditorPanel.kUndo"));
	string $redo					= (uiRes("m_scriptEditorPanel.kRedo")); 
	string $cut						= (uiRes("m_scriptEditorPanel.kCut")); 
	string $copy					= (uiRes("m_scriptEditorPanel.kCopy")); 
	string $paste					= (uiRes("m_scriptEditorPanel.kPaste"));
	string $selectAll				= (uiRes("m_scriptEditorPanel.kSelectAll"));
	string $clearHistory			= (uiRes("m_scriptEditorPanel.kClearHistory"));
	string $clearInput				= (uiRes("m_scriptEditorPanel.kClearInput"));
	string $clearAll				= (uiRes("m_scriptEditorPanel.kClearAll"));
	string $goto					= (uiRes("m_scriptEditorPanel.kGoto"));
	string $indentSel				= (uiRes("m_scriptEditorPanel.kIndentSelection"));
	string $unindentSel				= (uiRes("m_scriptEditorPanel.kUnindentSelection"));
	// show
	string $showHistory				= (uiRes("m_scriptEditorPanel.kShowHistory"));
	string $showInput				= (uiRes("m_scriptEditorPanel.kShowInput"));
	string $showBoth				= (uiRes("m_scriptEditorPanel.kShowBoth"));
	string $searchAndReplace		= (uiRes("m_scriptEditorPanel.kSearchAndReplace"));
	// history
	string $batchRenderMessages		= (uiRes("m_scriptEditorPanel.kBatchRenderMessages"));
	string $echoAllCommands			= (uiRes("m_scriptEditorPanel.kEchoAllCommands"));
	string $showErrorLineNumbers	= (uiRes("m_scriptEditorPanel.kLineNumbersInErrors"));
	string $showStackTrace			= (uiRes("m_scriptEditorPanel.kShowStackTrace"));
	string $suppressCommandResults	= (uiRes("m_scriptEditorPanel.kSuppressCommandResults"));
	string $suppressInfoMessages	= (uiRes("m_scriptEditorPanel.kSuppressInfoMessages"));
	string $suppressWarningMessages = (uiRes("m_scriptEditorPanel.kSuppressWarningMessages"));
	string $suppressErrorMessages	= (uiRes("m_scriptEditorPanel.kSuppressErrorMessages"));
	string $suppressDupVarMessages	= (uiRes("m_scriptEditorPanel.kSuppressDupVarMessages"));
	string $suppressStackWindow		= (uiRes("m_scriptEditorPanel.kSuppressStackWindow"));
	string $filterOutput			= (uiRes("m_scriptEditorPanel.kFilterOutput"));
	// command
	string $showLineNumbers			= (uiRes("m_scriptEditorPanel.kShowLineNumbers"));
	string $useTabsForIndent		= (uiRes("m_scriptEditorPanel.kUseTabsForIndent"));	
	string $autoCloseBraces			= (uiRes("m_scriptEditorPanel.kAutoCloseBraces"));	
	string $showQuickHelp			= (uiRes("m_scriptEditorPanel.kShowQuickHelp"));
	string $commandCompletion			= (uiRes("m_scriptEditorPanel.kCommandCompletion"));
	string $pathCompletion			= (uiRes("m_scriptEditorPanel.kPathCompletion"));
	string $toolTipHelp			= (uiRes("m_scriptEditorPanel.kToolTipHelp"));
	string $showCommandHelp			= (uiRes("m_scriptEditorPanel.kShowCommandHelp"));
	string $execute					= (uiRes("m_scriptEditorPanel.kExecute"));
	string $executeAll				= (uiRes("m_scriptEditorPanel.kExecuteAll"));
	// tabs
	string $tabName					= (uiRes("m_scriptEditorPanel.kTabName"));
	string $tabNameWarning			= (uiRes("m_scriptEditorPanel.kInvalidTabNameWarning"));
	string $addTab					= (uiRes("m_scriptEditorPanel.kAddTab"));
	string $rename					= (uiRes("m_scriptEditorPanel.kRename"));
	//
	string $searchError				= (uiRes("m_scriptEditorPanel.kSearchFailed"));
}

global proc
addScriptEditorPanel2 (string $whichPanel)
//
//  Description:mp
//		Add the panel to a layout.
//		Parent the editors to that layout and create any other
//		controls required.
//
{
	// Predefines
	scriptEditorPredefines;
	//
	global int $gScriptEditorMenuBarVisible;
	global string $gCommandPopupMenus[];
		
	global string $gCommandLayout;
	global string $gCommandReporter;
	global string $gCommandExecuter[];
	global string $gCommandExecuterLayout[];
	global string $gCommandExecuterName[];
	global string $gCommandExecuterType[];
	global string $gLastFocusedCommandExecuter;
	global string $gLastFocusedCommandReporter;
	global string $gLastFocusedCommandControl;

	$gScriptEditorMenuBarVisible = 1;
	$gLastFocusedCommandControl = "";
	$gLastFocusedCommandReporter = "";
	$gLastFocusedCommandExecuter = "";

	$gCommandExecuterLayout = {};
	$gCommandExecuter = {};
	$gCommandPopupMenus = {};

	global string $gCommandExecuterTabs;
	global string $gCommandExecuterTabsPane;
	string $editorControl = ($whichPanel + "EditorControl");

    int $hasPython = `exists python`;

	// Make sure that there is no template active
	setUITemplate -pushTemplate NONE;

	// clear the option vars from before first;
	if (size($gCommandExecuter) == 0) {
		// on the first instance of the script editor, we load the arrays from the option vars
        if (`optionVar -exists ScriptEditorExecuterTypeArray`) {
			// We first load them into temporary arrays and then make sure that we
			// don't have any that are file's which are duplicated in array.
			string $tempCommandExecuterName[] = `optionVar -q ScriptEditorExecuterLabelArray`;
			string $tempCommandExecuterType[] = `optionVar -q ScriptEditorExecuterTypeArray`;
			clear($gCommandExecuterName);
			clear($gCommandExecuterType);

			int $len = size($tempCommandExecuterName);
			int $i;
			int $index;
			for ($i = 0; $i < $len; ++$i) {
				// If this item points to a file, make sure we don't already have it.
				// If this item points to a scratch tab, just add it.
				if (isFullPathToScriptFile($tempCommandExecuterName[$i], "-r")) {
					if (0 == stringArrayContains($tempCommandExecuterName[$i], $gCommandExecuterName)) {
						$gCommandExecuterName[$index] = $tempCommandExecuterName[$i];
						$gCommandExecuterType[$index] = $tempCommandExecuterType[$i];
						$index++;
					}
				} else {
					$gCommandExecuterName[$index] = $tempCommandExecuterName[$i];
					$gCommandExecuterType[$index] = $tempCommandExecuterType[$i];
					$index++;
				}
			}
		}
	}else {
		if (`optionVar -exists ScriptEditorExecuterTypeArray`) {
			optionVar -clearArray ScriptEditorExecuterLabelArray;
			optionVar -clearArray ScriptEditorExecuterTypeArray;
		}
	}

	// Define the standard panel
	//
	string $widgetList[];

	$widgetList[2] = `scriptedPanel -query -control $whichPanel`;
	$widgetList[0] = `formLayout`;
	$widgetList[3] = `frameLayout -visible true -borderVisible false
			-labelVisible false -collapsable false -collapse true`;
	$widgetList[4] = `formLayout -visible true`;
	$widgetList[5] = `flowLayout -columnSpacing 4`;
	setParent $widgetList[0];
	$widgetList[6] = `formLayout -visible true`;

	formLayout -edit
		-attachForm $widgetList[3] top 0 
		-attachForm $widgetList[3] right 0
		-attachForm $widgetList[3] left 0

		-attachControl $widgetList[6] top 0 $widgetList[3]
		-attachForm $widgetList[6] bottom 0
		-attachForm $widgetList[6] right 0
		-attachForm $widgetList[6] left 0
		$widgetList[0];

	setParent $widgetList[0];

	
	// Add tools to the tool layout
	//
	int $iconSize = 23;
	setParent $widgetList[5];
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kLoadScript"))
			-image "openScript.png"
			-command "handleScriptEditorAction \\"load\\""
			openScriptButton;
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kSourceScript"))
			-image "sourceScript.png"
			-command "handleScriptEditorAction \\"source\\""
			sourceScriptButton;
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kSaveScript"))
			-image "save.png"
			-command "handleScriptEditorAction \\"save\\""
			saveScriptButton;
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kSaveScriptToShelf"))
			-image "saveToShelf.png"
			-command "handleScriptEditorAction \\"saveToShelf\\""
			saveScriptToShelfButton;

		separator -height $iconSize -horizontal false -style single fileSeperator;

		iconTextButton 
			-width $iconSize -height$iconSize
			-annotation (uiRes("m_scriptEditorPanel.kClearHistory"))
			-image "clearHistory.png"
			-command "handleScriptEditorAction \\"clearHistory\\""
			clearHistoryButton;
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kClearInput"))
			-image "clearInput.png"
			-command "handleScriptEditorAction \\"clearInput\\""
			clearInputButton;
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kClearAll"))
			-image "clearAll.png"
			-command "handleScriptEditorAction \\"clearAll\\""
			clearAllButton;

		separator -height $iconSize -horizontal false -style single clearSeperator;

		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kShowHistory"))
			-image "showHistory.png"
			-command "handleScriptEditorAction \\"maximizeHistory\\""
			showHistoryButton;
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kShowInput"))
			-image "showInput.png"
			-command "handleScriptEditorAction \\"maximizeInput\\""
			showInputButton;
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kShowBoth"))
			-image "showBoth.png"
			-command "handleScriptEditorAction \\"maximizeBoth\\""
			showBothButton;

		separator -height $iconSize -horizontal false -style single showSeperator;

		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kEchoAllCommands"))			
			-command "handleScriptEditorAction \\"echoAllCommands\\""
			echoAllCommandsButton;
		// echo all commands initial icon state
		if (`optionVar -exists echoAllLines`) {
			string $icon = (`optionVar -q echoAllLines` ? "echoCommands.png" : "echoCommandsOff.png");
			iconTextButton -e -image $icon echoAllCommandsButton;
		}	

		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kShowLineNumbers"))			
			-command "handleScriptEditorAction \\"showLineNumbers\\""
			showLineNumbersButton;
		// show line numbers initial icon state
		if (`optionVar -exists commandExecuterShowLineNumbers`) {
			string $icon = (`optionVar -q commandExecuterShowLineNumbers` ? "showLineNumbers.png" : "showLineNumbersOff.png");
			iconTextButton -e -image $icon showLineNumbersButton;
		}

		separator -height $iconSize -horizontal false -style single optionsSeperator;

		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kExecuteAll"))
			-image "executeAll.png"
			// -command "handleScriptEditorAction \\"executeAll\\""
			-command "python \\"global __scriptEditorExecuteAll;__scriptEditorExecuteAll()\\""
			executeAllButton;
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kExecute"))
			-image "execute.png"
			// -command "print \\"execute\\""
			-command "python \\"global __scriptEditorExecute;__scriptEditorExecute()\\""
			executeButton;


		separator -height $iconSize -horizontal false -style single executeSeperator;

		textField 
			-width 120 -height 20
			-annotation (uiRes("m_scriptEditorPanel.kSASToolbarField"))
			-enterCommand "searchAndSelectToolbarCmd(true)"
			-alwaysInvokeEnterCommandOnReturn true
			scriptEditorToolbarSearchField;
		popupMenu -postMenuCommand "searchAndSelectToolbarPopupUpdate" 
			scriptEditorToolbarSearchFieldPopupMenu;	
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kSASToolbarDownButton"))
			-image "searchDown.png"
			-command "searchAndSelectToolbarCmd(true)"
			scriptEditorToolbarSearchDownButton;
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kSASToolbarUpButton"))
			-image "searchUp.png"
			-command "searchAndSelectToolbarCmd(false)"
			scriptEditorToolbarSearchDownUp;

		separator -height $iconSize -horizontal false -style single searchSeperator;

		textField 
			-width 30 -height 20
			-annotation (uiRes("m_scriptEditorPanel.kGotoLineToolbarField"))
			-enterCommand "gotoLineToolbarCmd"
			-alwaysInvokeEnterCommandOnReturn true
			scriptEditorToolbarGotoField;
		popupMenu -postMenuCommand "gotoLineToolbarPopupUpdate" 
			scriptEditorToolbarGotoFieldPopupMenu;							
		iconTextButton 
			-width $iconSize -height $iconSize
			-annotation (uiRes("m_scriptEditorPanel.kGotoLineToolbarButton"))
			-image "gotoLine.png"
			-command "gotoLineToolbarCmd"
			scriptEditorToolbarGotoLineButton;
		

	int $formMargin = 2;
	//	Layout the toolbar
	//
	setParent $widgetList[4];
	formLayout -edit
		-attachForm	$widgetList[5] "left"	$formMargin
		-attachForm $widgetList[5] "top"    $formMargin
		-attachForm $widgetList[5] "bottom" $formMargin
		-attachForm $widgetList[5] "right"  0
		
		$widgetList[4];
	// Parent the editors to the editor layout
	//
	setParent $widgetList[6];

	{
		// build the panels first
		$gCommandLayout = `paneLayout -configuration "horizontal2"`;
			$gCommandReporter = `cmdScrollFieldReporter -width 20 -height 20`;
			cmdScrollFieldReporter -e -receiveFocusCommand ("setLastFocusedCommandReporter " + $gCommandReporter) $gCommandReporter;	
				$gCommandPopupMenus[size($gCommandPopupMenus)] = `popupMenu -markingMenu true -postMenuCommand "verifyCommandPopupMenus"`;
				buildScriptEditorCondensedPopupMenus($gCommandPopupMenus[size($gCommandPopupMenus)-1], true);		
				loadCommandReporterOptionVars($gCommandReporter);

			setLastFocusedCommandReporter $gCommandReporter;

			$gCommandExecuterTabsPane = `paneLayout -configuration "vertical2" -staticWidthPane 2`;
			$gCommandExecuterTabs = `tabLayout -selectCommand "selectCurrentExecuterControl" -showNewTab true
										-newTabCommand "handleScriptEditorAction \\"addExecuterTab\\""
										-borderStyle "none"`;
			if (size($gCommandExecuterName) == 0) {
				// build all new	
				buildNewExecuterTab(-1, "MEL", "mel", 0);
				if ($hasPython) {
					buildNewExecuterTab(-1, "Python", "python", 0);
				}
			}else {
				// don't need to update name, just build with the other info
				int $len = size($gCommandExecuterName);
				int $i;
				for ($i = 0; $i < $len; ++$i) {
					buildNewExecuterTab($i, $gCommandExecuterName[$i], $gCommandExecuterType[$i], 0);
				}
			}

			if (size($gCommandExecuterName) > 0)
				setLastFocusedCommandExecuter $gCommandExecuter[0];

			// help sidebar
			setParent $gCommandExecuterTabsPane;

			global string $gCommandExecuterSideBar;
			global string $gCommandExecuterSideBarHelpForm;
			global string $gCommandExecuterSideBarHelpField;
			global string $gCommandExecuterSideBarHelpResults;
			global int $gCommandExecuterShowQuickHelp;

			$gCommandExecuterSideBar = `tabLayout`;
			$gCommandExecuterSideBarHelpForm = `formLayout -width 120`;
				$gCommandExecuterSideBarHelpField = `textField -height 24 -enterCommand "showFieldCmdQuickHelp" -alwaysInvokeEnterCommandOnReturn true`;
				$gCommandExecuterSideBarHelpResults = `textScrollList -doubleClickCommand "doubleClickCmdQuickHelp" -allowMultiSelection on`;

					// popup menu to hide quick help
					popupMenu;
						menuItem -radialPosition "N"
								-label (uiRes("m_scriptEditorPanel.kShowDetailedHelp"))
								-command "showFieldCmdDocumentation";
						menuItem -radialPosition "S"
								-label (uiRes("m_scriptEditorPanel.kHideQuickHelp"))
								-command "toggleCmdQuickHelp(0, 0)";
			
			tabLayout -e -tabLabel $gCommandExecuterSideBarHelpForm (uiRes("m_scriptEditorPanel.kQuickHelp")) $gCommandExecuterSideBar;
			
			formLayout -e 
						-attachForm $gCommandExecuterSideBarHelpField top 0
						-attachForm $gCommandExecuterSideBarHelpField left 0
						-attachForm $gCommandExecuterSideBarHelpField right 0
						-attachNone $gCommandExecuterSideBarHelpField bottom

						-attachControl $gCommandExecuterSideBarHelpResults top 2 $gCommandExecuterSideBarHelpField
						-attachForm $gCommandExecuterSideBarHelpResults left 0
						-attachForm $gCommandExecuterSideBarHelpResults right 0
						-attachForm $gCommandExecuterSideBarHelpResults bottom 0

					$gCommandExecuterSideBarHelpForm;
		
			// show and attach forms accordingly
			// NOTE: move formLayout attachments out of func if we add new side bars!
			toggleCmdQuickHelp($gCommandExecuterShowQuickHelp, 1);

		formLayout -e 
					-attachForm $gCommandLayout left 0
					-attachForm $gCommandLayout right 0
					-attachForm $gCommandLayout top 0
					-attachForm $gCommandLayout bottom 0 $widgetList[6];
	}

	//	menuBarLayout is turned on for this editor -
	//	create the top level menus
	//
	setParent $widgetList[2];

	// build the menus
	{ 
		global string $gScriptEditorMenuBarPrefix;
		buildScriptEditorMenus($widgetList[2], $gScriptEditorMenuBarPrefix, false, false);

		addContextHelpProc $whichPanel "buildScriptEditorContextHelpItems";
		doHelpMenu $whichPanel $whichPanel;
	}

	// select the previous executer tab (if one was saved)
	//
	if (`optionVar -exists ScriptEditorExecuterTabIndex`) {
		int $prevIdx = `optionVar -q ScriptEditorExecuterTabIndex`;
		if ( (0 < $prevIdx) && ($prevIdx <= `tabLayout -q -numberOfChildren $gCommandExecuterTabs`) ) {
			tabLayout -e -selectTabIndex $prevIdx $gCommandExecuterTabs;
		}
	}

	setUITemplate -popTemplate;

	selectCurrentExecuterControl;

	scriptJob -parent $whichPanel -event "quitApplication" ("removeScriptEditorPanel " + $whichPanel);
}

''')

cmds.scriptedPanelType( 'scriptEditorPanel', e=1, addCallback='addScriptEditorPanel2' )
