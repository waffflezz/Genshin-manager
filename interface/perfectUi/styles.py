style_bt_standard = (
            """
            QPushButton {
                background-image: ICON_REPLACE;
                background-position: left center;
                background-repeat: no-repeat;
                border: none;
                color: rgb(200, 200, 200);
                border-left: 22px solid rgb(27, 29, 35);
                background-color: rgb(27, 29, 35);
                text-align: left;
                padding-left: 45px;
            }
            QPushButton[Active=true] {
                background-image: ICON_REPLACE;
                background-position: left center;
                background-repeat: no-repeat;
                border: none;
                border-left: 22px solid rgb(27, 29, 35);
                border-right: 45px solid rgb(44, 49, 60);
                background-color: rgb(27, 29, 35);
                text-align: left;
                padding-left: 45px;
            }
            QPushButton:hover {
                background-color: rgb(33, 37, 43);
                border-left: 22px solid rgb(33, 37, 43);
            }
            QPushButton:pressed {
                background-color: rgb(85, 170, 255);
                border-left: 22px solid rgb(85, 170, 255);
            }
            """
        )