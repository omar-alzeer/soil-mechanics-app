; The name of the installer
Name "soil"

; The file to write
OutFile "soil.exe"

; Request application privileges for Windows Vista
RequestExecutionLevel user

; Build Unicode installer
Unicode True

; The default installation directory
InstallDir $DESKTOP\soil

;--------------------------------

; Pages

Page directory
Page instfiles

;--------------------------------

!define SHCNE_ASSOCCHANGED 0x08000000
!define SHCNF_IDLIST 0
 
Function RefreshShellIcons
  ; By jerome tremblay - april 2003
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v \
  (${SHCNE_ASSOCCHANGED}, ${SHCNF_IDLIST}, 0, 0)'
FunctionEnd

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /nonfatal /a /r "soil\"
  
SectionEnd

Section

WriteRegStr HKCU "Software\Classes\.soil" "" "soilApp"
WriteRegStr HKCU "Software\Classes\soilApp" "" "My soil App"
WriteRegStr HKCU "Software\Classes\soilApp\DefaultIcon" "" "$INSTDIR\Icons\soil.ico"
WriteRegStr HKCU "Software\Classes\soilApp\shell\open\command" "" '"$INSTDIR\app.bat" "%1"'

Call RefreshShellIcons

SectionEnd