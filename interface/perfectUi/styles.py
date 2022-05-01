style_bt_standard = (
            """
            QPushButton {
                background-image: ICON_REPLACE;
                background-position: left center;
                background-repeat: no-repeat;
                border: none;
				color: rgb(33, 53, 57);
                border-left: 22px solid rgb(120, 193, 207);
	            background-color: rgb(120, 193, 207);
                text-align: left;
                padding-left: 45px;
				border-radius: 12px;
            }
            QPushButton[Active=true] {
                background-image: ICON_REPLACE;
                background-position: left center;
                background-repeat: no-repeat;
                border: none;
                border-left: 22px solid  rgb(120, 193, 207);
                border-right: 45px solid rgb(120, 193, 207);
                background-color: rgb(120, 193, 207);
                text-align: left;
                padding-left: 45px;
				border-radius: 12px;
            }
            QPushButton:hover {
				background-color: rgb(109, 176, 188);
                border-left: 22px solid rgb(109, 176, 188);
				border-radius: 12px;
            }
            QPushButton:pressed {
				background-color: rgb(129, 209, 223);
                border-left: 22px solid rgb(129, 209, 223);
				border-radius: 12px;
            }
            """
        )