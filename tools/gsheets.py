import gspread as gs


class GSheetClient:
    def __init__(self, cred: str) -> None:
        self.gc = gs.service_account(filename=cred)

    def get_sheet(self, sheet_key: str) -> gs.Spreadsheet:
        return self.gc.open_by_key(sheet_key)
