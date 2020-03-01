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
    SaveBtn: TButton;
    LoadButton: TButton;
    ControlPanel: TPanel;
    ImageDraw: TImage;
    ImagePanel: TPanel;
    ImageBox: TScrollBox;
    DrawTimer: TTimer;
    OpenDialog: TOpenDialog;
    SaveDialog: TSaveDialog;
    procedure DrawTimerTimer(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure ImageDrawMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure LoadButtonClick(Sender: TObject);
    procedure SaveBtnClick(Sender: TObject);
  private

  public

  end;

var
  MainForm: TMainForm;
  Boxes: array[0..4096] of TRect;
  BoxesCount: Integer;
  Adding: Boolean;
  AddingBox: TRect;

implementation

{$R *.lfm}

{ TMainForm }

procedure TMainForm.LoadButtonClick(Sender: TObject);
begin
  if OpenDialog.Execute then
  begin
       ImageDraw.Picture.LoadFromFile(OpenDialog.FileName);
  end;
end;

procedure TMainForm.SaveBtnClick(Sender: TObject);
var
  OutFile: TStringList;
  X: Integer;
begin
  if SaveDialog.Execute then
  begin
    OutFile:= TStringList.Create();
    for X:= 0 to BoxesCount - 1 do begin
      OutFile.Add(IntToStr(Boxes[X].Right) + ' ' +
                  IntToStr(Boxes[X].Top) + ' ' +
                  IntToStr(Boxes[X].Left) + ' ' +
                  IntToStr(Boxes[X].Bottom));
    end;
    OutFile.SaveToFile(SaveDialog.FileName);
  end;
end;

procedure TMainForm.ImageDrawMouseDown(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
  if Adding then begin
    Adding := False;
    AddingBox.BottomRight := TPoint.Create(X, Y);
    Boxes[BoxesCount] := AddingBox;
    inc(BoxesCount);
  end else begin
    Adding := True;
    AddingBox := TRect.Create(X, Y, 0, 0);
  end;
end;


procedure TMainForm.DrawTimerTimer(Sender: TObject);
var
  X: Integer;
begin
  for X := 0 to BoxesCount - 1 do begin
    with ImageDraw.Picture.Bitmap.Canvas do begin
      Brush.Style:= BSClear;
      Pen.Color:= clRED;
      Pen.Width:= 2;
      Font.Color:= clRed;
      Font.Size:= 12;
      Rectangle(Boxes[X]);
      TextOut(Boxes[X].Left, Boxes[X].Bottom, 'Oil tank ' + IntToStr(X + 1));
    end;
  end;
end;

procedure TMainForm.FormCreate(Sender: TObject);
begin
  BoxesCount:= 0;
  Adding:= False;
end;

end.

