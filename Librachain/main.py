import pytermgui as ptg

class Registration:

    CONFIG = """
    config:
        InputField:
            styles:
                prompt: dim italic
                cursor: '@72'
        Label:
            styles:
                value: dim bold

        Window:
            styles:
                border: '60'
                corner: '60'

        Container:
            styles:
                border: '96'
                corner: '96'
    """

    with ptg.YamlLoader() as loader:
        loader.load(CONFIG)

    with ptg.WindowManager() as manager:
        window = (
            ptg.Window(
                "",
                ptg.InputField("", prompt="Private Key: "),
                ptg.InputField("", prompt="Username: "),
                ptg.InputField("", prompt="Password: "),
                ptg.InputField("", prompt="Password Confirmation: "),
                "",
                ["Submit"],
                width=60,
                box="DOUBLE",
            )
            .set_title("[210 bold]Registration")
            .center()
        )

        manager.add(window)