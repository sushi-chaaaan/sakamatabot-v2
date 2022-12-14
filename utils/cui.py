class CommandLineUtils:
    @classmethod
    def y_or_n(cls, message: str, *, default: bool | None = None) -> bool:
        """CUIでy/nを聞く

        Args:
            message (str): 質問文
            default (bool, optional): デフォルト値. TrueならY/n, Falseならy/N, Noneならy/n

        Returns:
            bool: yならTrue、nならFalse
        """
        while True:
            prompt = "Y/n" if default is True else "y/N" if default is False else "y/n"
            ans = input(f"{message} [{prompt}] ")
            if ans == "":
                if default is None:
                    print("yかnを入力してください。")
                    continue
                else:
                    return default
            elif ans == "y":
                return True
            elif ans == "n":
                return False
            else:
                print("yかnを入力してください。")


if __name__ == "__main__":
    print(CommandLineUtils.y_or_n("test", default=True))
