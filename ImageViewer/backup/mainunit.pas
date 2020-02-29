unit MainUnit;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, ExtCtrls, StdCtrls;

const
  ImagePath = '../Source/merged/';

type

  { TMainForm }

  TMainForm = class(TForm)
    LoadButton: TButton;
    ControlPanel: TPanel;
    ImageDraw: TImage;
    ImagePanel: TPanel;
    ImageBox: TScrollBox;
    procedure LoadButtonClick(Sender: TObject);
  private

  public

  end;

var
  MainForm: TMainForm;

implementation

{$R *.lfm}

{ TMainForm }

procedure TMainForm.LoadButtonClick(Sender: TObject);
begin
  ImageDraw.LoadFromFile(ImagePath + 'US Oil Indianapolis IN_screen__merged.jpg');
end;

end.

