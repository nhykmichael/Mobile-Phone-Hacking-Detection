import datetime
import importlib
import random
import time
from tkinter import ttk
import string

"""
Prototype for Firmware/Hardware Mobile Phone Hacking Detection Tool Interface

Author: [Michael Nhyk Ahimbisibwe]
System Name: [Mobile Phone Firmware Hardware Hacking Detection]
Model: [BSC HON YEAH PROJECT 1.0]
"""

import customtkinter
from FirmwareHackDetector import *
from InterfaceHub import IUserInterface, IDeviceConnector

customtkinter.set_appearance_mode("dark")  # Mode can be Light or Dark
# customtkinter.set_default_color_theme("blue")  # Can be blue , green or dark blue

devices = get_adb_devices()

customtkinter.set_default_color_theme('blue')
immediate_dir: str = f"C:\\Android\\DetectHacking\\{prop[0]}_{prop[1]}_{prop[2]}"


def change_theme_event(strMode: str):
    current_theme = customtkinter.get_appearance_mode()
    customtkinter.set_appearance_mode(strMode)
    print(f"Theme change from '{COLOR[2]}{current_theme}{COLOR[4]}' to '{COLOR[2]}{strMode}'{COLOR[4]}")


def change_scaling_event(strNewScaling: str):
    intNewScalingDouble = int(strNewScaling.replace("%", "")) / 100.0
    customtkinter.set_widget_scaling(intNewScalingDouble)


def frame(frame_, text: str):
    text_box = customtkinter.CTkTextbox(frame_, width=140, height=140, font=("Calibre", 13, "roman"),
                                        fg_color="#4c6e81")
    text_box.insert("1.0", text.format("Calibre", 13, "italic"))
    return text_box


def shorter_frame(frame_, text: str):
    text_box = customtkinter.CTkTextbox(frame_, width=130, height=80, font=("Calibre", 13, "roman"),
                                        fg_color="#4c6e81")
    text_box.insert("1.0", text.format("Calibre", 13, "italic"))
    return text_box


def create_phone_files_folder():
    # Create a folder for the device
    _phone = Phone()
    model = _phone.return_phone_model()
    name = _phone.return_manufacture()
    serial = get_device_info("ro.boot.serialno")

    folder_path = f"C:\\Android\\DetectHacking\\{name}_{model}_{serial}"

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path
    # End of create folder for this device (will this work effectively in create specified folder)


# print(create_phone_files_folder())


def detect_patch_level():
    patch = FirmwareAnalyser(None)
    directory = immediate_dir  # "C:\\Android\\DetectHacking\\SAMSUNG_SM-N986B_R5CN80EC24J"
    patch.security_patch_level_analysis(directory, "device_properties.txt", 6)
    # FirmwareAnalyser.security_patch_level_analysis(directory, "device_properties.txt", 6)


def boot_state_analysis():
    prop_dir = '\\device_properties.txt'
    boot_state = FirmwareAnalyser(immediate_dir + prop_dir)
    print(boot_state.boot_state)


def SELinux_analysis():
    prop_dir = '\\device_properties.txt'
    SELinux_state = FirmwareAnalyser(immediate_dir + prop_dir)
    print(SELinux_state.SELinuxStatus)


def rooted_state():
    root_state_results = FirmwareAnalyser(None)
    root_state_results.root_state_analysis(immediate_dir + "\\device_properties.txt")


# To be used in status changer...
def set_widgets_status_in_frame(_frame, status):
    for child in _frame.winfo_children():
        if status == 'enabled':
            child.configure('normal')
        elif status == 'disabled':
            child.configure('disabled')


class SystemUserInterface(IUserInterface, IDeviceConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app_list = None
        self.side_bar_text_area = None  # Added later ....
        self.mobile_phone_graphics = None  # Added later ....
        self.hardware_analysis_tabs = []
        self.buttons = []
        self.root_ctk = customtkinter.CTk()
        self.root_ctk.geometry(f"{1150}x{588}")
        self.main_frame_color = None
        self.main_color_changer(0)  # This changes the phone graphics status (Active, Inactive
        self.live_text = None

        self.app_drop_down_menu = None
        self.drop_down_apps = None
        self.select_model = None
        self.drop_down_model_var = None

        # TEXT BOXES
        self.firmware_analysis_text_box = None
        self.hardware_analysis_text_box = None
        self.general_textbox = None
        self.firmware_text_box = None
        self.hardware_text_box = None
        self.hacking_text_box = None
        self.help_menu_text = None

        self.random_forest_pre_trained = None

        #
        self.root_ctk.title(self.__class__.__name__)
        self.root_ctk.iconbitmap("uj_or.ico")

        # Configure the root_ctk grid , this will span the sidebar all the way ###### SIDE BAR
        self.root_ctk.grid_rowconfigure(0, weight=1)
        self.root_ctk.grid_columnconfigure(1, weight=1)

        self.sideBarFrame = customtkinter.CTkFrame(self.root_ctk, width=145, corner_radius=0)
        self.sideBarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sideBarFrame.grid_rowconfigure(4, weight=1)

        # Sidebar objects

        self.initial_buttons_title = customtkinter.CTkLabel(self.sideBarFrame, text="Attach Phone",
                                                            font=customtkinter.CTkFont(size=16, weight="bold"),
                                                            anchor="w")
        self.initial_buttons_title.grid(row=0, column=0, padx=18, pady=(18, 10))

        # Connect Device Button
        self.connect_button = customtkinter.CTkButton(self.sideBarFrame, text="Connect Phone", fg_color="#006600",
                                                      hover_color="#3EA055", command=self.connect_device)
        self.connect_button.grid(row=1, column=0, padx=20, pady=(20, 10))  # Alternative

        # Disconnect Device Button
        self.disconnect_button = customtkinter.CTkButton(self.sideBarFrame, text="Disconnect Device")
        self.disconnect_button.grid(row=2, column=0, padx=20, pady=20)
        self.state_all('disabled')
        '''self.disconnect_button.configure(state="disabled")'''

        # Create the font style object----------------Side Bar Text Box ----------------------------------
        self.side_bar_text_box = frame(self.sideBarFrame, "Connect device")  # Text area in the sidebar
        # Insert the default text at the beginning of the textbox
        # self.side_bar_text_box.insert("1.0", "No Phone is connected".format("Arial", 12, "italic"))
        # Apply the default text style to the placeholder
        self.side_bar_text_box.grid(row=3, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.help_button = customtkinter.CTkButton(self.sideBarFrame, text="Help", fg_color="#CC3300",
                                                   hover_color='#3D0C02',
                                                   command=self.save_and_read_help_menu_html)
        self.help_button.grid(row=4, column=0, padx=20, pady=15)

        # Theme switching

        # self.theme_switching = customtkinter.CTkLabel(self.sideBarFrame, text="Theme Switching:",
        #                                               font=customtkinter.CTkFont(size=12, weight="normal",
        #                                                                          slant="roman"), anchor="w")
        # self.theme_switching.grid(row=5, column=0, padx=20, pady=(10.0, 0.0))
        self.theme_switching_menu = customtkinter.CTkOptionMenu(self.sideBarFrame,
                                                                values=['Change Theme', "Light", "Dark", "System"],
                                                                command=change_theme_event)
        self.theme_switching_menu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Scaling
        self.scaling = customtkinter.CTkLabel(self.sideBarFrame, text="UI Scaling:",
                                              font=customtkinter.CTkFont(size=12, weight="normal", slant="roman"),
                                              anchor="w")
        self.scaling.grid(row=7, column=0, padx=20, pady=(15.0, 0.0))
        self.scaling_menu = customtkinter.CTkOptionMenu(self.sideBarFrame,
                                                        values=["90", "100", "110"],
                                                        command=change_scaling_event)
        self.scaling_menu.grid(row=8, column=0, padx=20, pady=(10.0, 20.0))

        # Main Screen Area

        # ------------------------ GENERAL TAB VIEW COL 2 ROW 2 --------------------------
        self.general_textbox = frame(None, "No Action Made (Notifications Will Show Here)\n")  # Text area
        self.general_textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.general_textbox.insert(tk.END, global_text_green + '\n')

        self.general_tab_view = customtkinter.CTkTabview(self.root_ctk, width=360)
        general_tab = self.general_tab_view.add("Pull Files")
        self.general_tab_view.grid(row=1, column=1, padx=(20, 0), pady=(20.0, 0), sticky="nsew")
        # Connection progress bar
        self.connection_progress = customtkinter.CTkLabel(general_tab, text="Phone Connecting:",
                                                          font=customtkinter.CTkFont(size=12, weight="normal",
                                                                                     slant="roman"), anchor="w")
        self.connection_progress.grid(row=0, column=0, padx=20, pady=(15.0, 0.0), sticky="nw")
        self.connection_progress_bar = customtkinter.CTkProgressBar(general_tab)
        self.connection_progress_bar.grid(row=0, column=0, padx=20.0, pady=(15.0, 0.0), sticky="nw")

        # Login Status
        self.login_status_button = customtkinter.CTkRadioButton(general_tab, text="Login Status", state='disabled')
        self.login_status_button.grid(row=0, column=1, padx=20, pady=(15.0, 0.0), sticky="ne")

        # Save files >>>

        # Drop down
        # Create a list of options for the drop-down menu
        options = ['Drop Down Select Pull File', 'Pull Permissions', 'Pull Apps List', 'Pull Properties',
                   'Pull Memory Usage Info', 'Pull Logcat', 'Pull AndroidManifest.xml']
        options_app = ['Drop Pull App Memory Dump', 'All Apps']
        # Create the drop-down menu widget
        self.drop_down_var = tk.StringVar()
        self.options_app_var = tk.StringVar()
        # self.drop_down_menu = ttk.Combobox(general_tab, textvariable=self.drop_down_var, values=options)
        self.drop_down_menu = customtkinter.CTkOptionMenu(general_tab, values=options, variable=self.drop_down_var,
                                                          dropdown_hover_color='#000000', dropdown_text_color='#C0C0C0',
                                                          dropdown_fg_color='#033E3E', fg_color='#006A4E', button_color=
                                                          '#004225', )
        self.pull_app_memo_dump_dropdown = customtkinter.CTkOptionMenu(general_tab, values=options_app,
                                                                       variable=self.options_app_var,
                                                                       dropdown_hover_color='#000000',
                                                                       dropdown_text_color='#C0C0C0',
                                                                       dropdown_fg_color='#033E3E',
                                                                       fg_color='#006A4E', button_color='#004225')
        # Set an initial value for the drop-down menu
        self.drop_down_menu.set(options[0])
        self.pull_app_memo_dump_dropdown.set(options_app[0])
        # Configure the appearance of the drop-down menu
        self.drop_down_menu.configure(font=customtkinter.CTkFont(size=15, weight="normal", slant="roman"), width=25)
        # Place the drop-down menu in the grid
        self.drop_down_menu.grid(row=1, column=0, padx=20, pady=(15.0, 0.0), sticky='nw')
        self.pull_app_memo_dump_dropdown.grid(row=4, column=0, padx=20, pady=(15.0, 0.0), sticky='nw')
        self.drop_down_menu.configure(state='disabled')
        self.pull_app_memo_dump_dropdown.configure(state='disabled')
        # Create the button for executing the selected option
        self.execute_button = customtkinter.CTkButton(general_tab, text="<- Pull File", width=22,
                                                      command=lambda: self.execute_selected_option())
        self.pull_app_memory_dump_button = customtkinter.CTkButton(general_tab, text="Pull Memo Dump", width=22,
                                                                   command=lambda: None)
        # self.execute_button.configure(bg_color='#FF0000')
        self.execute_button.grid(row=1, column=1, padx=10, pady=(15.0, 0.0), sticky='nw')
        self.pull_app_memory_dump_button.grid(row=4, column=1, padx=10, pady=(15.0, 0.0), sticky='nw')
        self.execute_button.configure(state="disabled")
        self.pull_app_memory_dump_button.configure(state="disabled")
        self.pull_android_manifest_button = customtkinter.CTkButton(general_tab, text="Pull App AndroidManifest",
                                                                    command=self.pull_AndroidManifest)
        self.pull_android_manifest_button.grid(row=3, column=0, padx=10, pady=(15.0, 0.0), sticky='sn')
        self.pull_android_manifest_button.configure(state='disabled')

        # ------------------------ MALWARE DETECTION TAB VIEW COL 2 ROW 2 --------------------------
        # malware_detection_tab = self.general_tab_view.add("Malware Detection")
        self.malware_detection('enabled')
        self.report('enabled')

        # ------------------------ EO MALWARE DETECTION TAB VIEW COL 2 ROW 2 -----------------------

        # Configure the root_ctk grid , this will span the sidebar all the way RIGHT
        self.initialize_tabview()  # Initial tab view elements
        self.sideBarFrameR = customtkinter.CTkFrame(self.root_ctk, width=15, corner_radius=0, fg_color="black")
        self.sideBarFrameR.grid(row=0, column=4, rowspan=4, sticky="nsew")
        self.sideBarFrameR.grid_rowconfigure(4, weight=1)

        # Configure the root_ctk grid , this will span the sidebar all the way BOTTOM
        self.initialize_tabview()  # Initial tab view elements
        self.sideBarFrameBottom = customtkinter.CTkFrame(self.root_ctk, height=10, corner_radius=0, fg_color="black")
        self.sideBarFrameBottom.grid(row=4, column=0, columnspan=5, sticky="nsew")
        self.sideBarFrameBottom.grid_columnconfigure(4, weight=1)

        self.mobile_phone_firmware_view_frame = customtkinter.CTkTabview(self.root_ctk, width=250, state='enabled')

        # self.side_bar_text_area.insert(tk.END, f"\n{self.live_text}")

        self.mobile_phone_view_frame = customtkinter.CTkTabview(self.root_ctk, width=250, state='enabled')

        self.mobile_phone_hacking_detector_view_frame = customtkinter.CTkTabview(self.root_ctk, width=250,
                                                                                 state='enabled')

        # Function to execute the selected option based on the drop-down menu value

    def state_all(self, state: str):
        self.disconnect_button.configure(state=state)
        # TOOLS
        # 0001 ***********************
        self.phone_hardware_firmware(state)
        # 0002 ***********************
        self.firmware_hardware_analysis(state)
        # 0002 ***********************
        self.firmware_hardware_hacking_detect(state)

        # MOBILE PHONE ************************************
        self.phone(state)

    def pull_AndroidManifest(self):
        self.general_textbox.insert(tk.END, "AndroidManifest Saved: C:\\Android\\DetectHacking\\...\\manifest\n")
        path = os.join(immediate_dir, 'clean_installed_package_list.txt')
        # app_list = AppSelector(immediate_dir + '\\' + 'clean_installed_package_list.txt', immediate_dir)
        app_list = AppSelector(path, immediate_dir)
        app_list.run()

    def execute_selected_option(self):
        selected_option = self.drop_down_var.get()
        directory = create_phone_files_folder()
        if selected_option == 'Pull Permissions':
            save_permissions(directory, 'permissions.txt')  # permissions saved in the directory
            self.general_textbox.insert(tk.END, "Permission saved in: C:\\Android\\DetectHacking\n")
        elif selected_option == 'Pull Apps List':
            dumpsys_ = os.join(immediate_dir, 'dumpsys_package_list.txt')
            dumpsys__ = os.join(immediate_dir, 'clean_installed_package_list.txt')
            # apps = PullPackage(immediate_dir + '\\' + 'dumpsys_package_list.txt',
            #                    immediate_dir + '\\' + 'clean_installed_package_list.txt')
            apps = PullPackage(dumpsys_, dumpsys__)
            apps.run()
            self.general_textbox.insert(tk.END, "Installed App Logs Saved in: C:\\Android\\DetectHacking\n")
        elif selected_option == 'Pull Properties':
            prop_puller = PullProp(directory)
            prop_puller.pull_and_save_properties()
            self.general_textbox.insert(tk.END, "Properties Saved in: C:\\Android\\DetectHacking\n")
        elif selected_option == 'Pull Memory Usage Info':
            memory_info = pull_memory_usage_info()
            if memory_info:
                output_file_path = f"{immediate_dir}/memory_usage_info.txt"  # Update this path
                save_memory_usage_info_pulled(memory_info, output_file_path)
                print(f"{COLOR[3]}Memory information saved to {COLOR[2]}{output_file_path}{COLOR[4]}")
            self.general_textbox.insert(tk.END, "Memory Info Saved in: C:\\Android\\DetectHacking\n")
            print(f"{COLOR[1]}Memory information pulled{COLOR[4]}")
        elif selected_option == "Pull Logcat":
            puller = PullLogcat(immediate_dir)
            puller.extract_logcat()
            puller.reorganize_logcat()
            self.general_textbox.insert(tk.END, "Logcat saved: C:\\Android\\DetectHacking\n")
        elif selected_option == 'Pull AndroidManifest.xml':
            # apk_extractor = APKExtractor(package_name, immediate_dir)
            # apk_extractor.extract_apk()
            # apk_extractor.extract_AndroidManifest()
            # apk_extractor.delete_saved_package()
            pass

    # Sidebar text box

    def malware_detection(self, status):
        malware_detection_tab = self.general_tab_view.add("|Malware Detection|")
        # Drop down
        # Create a list of options for the drop-down menu
        # options = ['Drop Down Select Pull File', 'Pull Permissions', 'Pull Apps List', 'Pull Properties',
        #            'Pull Memory Info', 'Pull Logcat', 'Pull AndroidManifest.xml']
        options = read_text_file('apps.txt') + ['All Apps']
        self.drop_down_model_var = tk.StringVar()
        self.random_forest_pre_trained = ["apk_high.model", "apk_good.model"]
        # self.select_model = ttk.Combobox(malware_detection_tab, textvariable=self.drop_down_model_var,
        #                                  values=self.random_forest_pre_trained)
        self.select_model = \
            customtkinter.CTkOptionMenu(malware_detection_tab, variable=self.drop_down_model_var,
                                        values=self.random_forest_pre_trained, dropdown_hover_color='#000000',
                                        dropdown_text_color='#C0C0C0', dropdown_fg_color='#033E3E', fg_color='#006A4E',
                                        button_color='#004225')
        self.select_model.set('Select Model-->')
        self.select_model.grid(row=0, column=0, padx=20, pady=(15.0, 0.0), sticky="nw", )
        self.select_model.configure(font=customtkinter.CTkFont(size=15, weight="bold", slant="roman"),
                                    state=status, width=15)
        # Create the drop-down menu widget
        scan_saved_apk = customtkinter.CTkButton(malware_detection_tab, text="Analyse Saved APK ...",
                                                 state=status, command=self.scan_saved_apk)
        scan_saved_apk.grid(row=0, column=1, padx=20, pady=(10, 10))

        self.drop_down_apps = tk.StringVar()
        self.app_drop_down_menu = ttk.Combobox(malware_detection_tab, textvariable=self.drop_down_apps, values=options)
        # Set an initial value for the drop-down menu
        self.app_drop_down_menu.set('Drop Down To Select App')
        # Configure the appearance of the drop-down menu
        self.app_drop_down_menu.config(font=customtkinter.CTkFont(size=15, weight="normal", slant="roman"), width=40)
        # Place the drop-down menu in the grid
        self.app_drop_down_menu.grid(row=1, column=0, padx=20, pady=(15.0, 0.0), sticky="nw", columnspan=2)
        self.app_drop_down_menu.config(state=status)
        scan_app = customtkinter.CTkButton(malware_detection_tab, text="Scan App ...",
                                           state=status, command=lambda: self.scan_selected_app())
        scan_app.grid(row=2, column=0, padx=20, pady=(10, 10))
        scan_all_app = customtkinter.CTkButton(malware_detection_tab, text="Scan All Apps ...",
                                               state=status, command=None)
        scan_all_app.grid(row=2, column=1, padx=20, pady=(10, 10))

    def report(self, state):
        hacking_report_tab = self.general_tab_view.add("|Report and Stats|")

    def scan_saved_apk(self):
        print("Scan Saved APK ...")

    def scan_selected_app(self):
        selected_option = self.drop_down_apps.get()
        model = self.select_model.get()
        print(f"{selected_option}\t\t{model}")
        if selected_option == 'All Apps':
            print("Scan All Apps ...")
        else:
            print("Scan App ...")

    def pull_app_memory_dump(self):
        selected_app = self.pull_app_memo_dump_dropdown.get()
        print(f"{selected_app}")
        app_save_dir = os.join(immediate_dir, selected_app)  # This is the directory to save the app memory dump
        pull_app_memory_dump(selected_app, app_save_dir)  # This is the function to pull the app memory dump
        print("Pull App Memory Dump ...")

    def phone_hardware_firmware(self, state):
        # 0001 Mobile phone hardware and firmware flame****************************
        self.initialize_tabview()  # Initial tab view elements
        self.mobile_phone_view_frame = customtkinter.CTkTabview(self.root_ctk, width=250, state=state)
        self.mobile_phone_view_frame.grid(row=0, column=2, padx=(20, 0), pady=(20.0, 0), sticky="nsew")
        self.mobile_phone_view_frame.grid_rowconfigure(4, weight=1)
        mobile_phone_tab = self.mobile_phone_view_frame.add("Mobile Hardware")

        # status = ''
        # for child in self.mobile_phone_view_frame.winfo_children():
        #     if self.main_frame_color == "#6BD0FF" or self.main_frame_color == "#CC3300":
        #         child.configure("enabled")
        #         status = 'normal'
        #     else:  # self.main_frame_color == "#00538E":
        #         child.configure("disabled")
        # #         status = 'disabled'
        # status = 'normal' if self.main_frame_color in ["#6BD0FF", "#CC3300"] else 'disabled'
        # for child in self.mobile_phone_view_frame.winfo_children():
        #     child.configure(status)

        # status = 'normal' if self.main_frame_color in ["#6BD0FF", "#CC3300"] else 'disabled'
        status = self.object_state()
        set_widgets_status_in_frame(self.mobile_phone_view_frame, status)

        # Mobile phone flame button and other attributes
        phone_detect_button = customtkinter.CTkButton(mobile_phone_tab, text="Phone Hardware Detect", state=status,
                                                      command=self.get_hardware_details)
        phone_detect_button.grid(row=1, column=1, padx=20, pady=(10, 10))
        self.hardware_text_box = frame(mobile_phone_tab, "Phone Hardware >>>>\n ")
        self.hardware_text_box.grid(row=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.text_box(2, 1, mobile_phone_tab, "Phone Hardware >>>> ")

        # Mobile phone firmware flame button and other attributes
        mobile_phone_firmware_tab = self.mobile_phone_view_frame.add("Phone Firmware")
        detect_firmware = customtkinter.CTkButton(mobile_phone_firmware_tab, text="Firmware Detect", state=status,
                                                  command=self.get_firmware)
        detect_firmware.grid(row=1, column=1, padx=20, pady=(10, 10))
        self.firmware_text_box = frame(mobile_phone_firmware_tab, "Phone Firmware >>>>\n ")
        self.firmware_text_box.grid(row=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.text_box(2, 1, mobile_phone_firmware_tab, "Phone Firmware >>>> ")

    def firmware_hardware_analysis(self, state):
        self.initialize_tabview()  # Initial tab view elements
        self.mobile_phone_firmware_view_frame = customtkinter.CTkTabview(self.root_ctk, width=250, state=state)
        self.mobile_phone_firmware_view_frame.grid(row=0, column=3, padx=(20, 0), pady=(20.0, 0), sticky="nsew")
        self.mobile_phone_firmware_view_frame.grid_rowconfigure(4, weight=1)
        firmware_analysis = self.mobile_phone_firmware_view_frame.add("Firmware Analysis")

        status = 'normal' if self.main_frame_color in ["#6BD0FF", "#CC3300"] else 'disabled'
        for child in self.mobile_phone_firmware_view_frame.winfo_children():
            child.configure(status)

        firmware_analysis_button = customtkinter.CTkButton(firmware_analysis, text="Firmware Analyser", state=status,
                                                           command=self.analyseFirmware)
        firmware_analysis_button.grid(row=1, column=3, padx=20, pady=(10, 10))

        # Add text box
        self.firmware_analysis_text_box = frame(firmware_analysis, "Firmware Analysis >>\n")
        # Insert the default text at the beginning of the textbox
        # Apply the default text style to the placeholder
        self.firmware_analysis_text_box.grid(row=2, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        hardware_analysis = self.mobile_phone_firmware_view_frame.add("Hardware Analysis")
        hardware_analysis_button = customtkinter.CTkButton(hardware_analysis, text="Hardware Analyser", state=status,
                                                           command=self.analyseHardware)
        hardware_analysis_button.grid(row=1, column=3, padx=20, pady=(10, 10))
        # Add text box
        self.hardware_analysis_text_box = frame(hardware_analysis, "Phone Hardware Analysis >> ")
        self.hardware_analysis_text_box.grid(row=2, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.hardware_analysis_tabs.append(hardware_analysis)
        self.buttons.append(hardware_analysis_button)
        # hardware_analysis_button.grid_remove()

    def firmware_hardware_hacking_detect(self, state):
        # Mobile phone hack detector
        self.initialize_tabview()  # Initial tab view elements
        self.mobile_phone_hacking_detector_view_frame = customtkinter.CTkTabview(self.root_ctk, width=250, state=state)
        self.mobile_phone_hacking_detector_view_frame.grid(row=1, column=2, padx=(20, 0), pady=(20.0, 0), sticky="nsew")
        self.mobile_phone_hacking_detector_view_frame.grid_rowconfigure(4, weight=1)
        phone_hack_detecting = self.mobile_phone_hacking_detector_view_frame.add("Detect Hacking")

        status = self.object_state()
        set_widgets_status_in_frame(self.mobile_phone_hacking_detector_view_frame, status)

        firmware_hack_detect = customtkinter.CTkButton(phone_hack_detecting, text="Detect Hardware Hacking",
                                                       state=status, command=self.detect_hack_firmware)
        firmware_hack_detect.grid(row=1, column=3, padx=20, pady=(10, 10))

        hardware_hack_detect = customtkinter.CTkButton(phone_hack_detecting, text="Detect Firmware Hacking",
                                                       state=status, command=self.detect_hack_hardware)
        hardware_hack_detect.grid(row=2, column=3, padx=20, pady=(10, 10))
        # self.text_box_shorter_height(3, 3, phone_hack_detecting, "Hacking Detecting >>>")
        self.hacking_text_box = shorter_frame(phone_hack_detecting, "Hacking Detecting >>>\n ")
        self.hacking_text_box.grid(row=3, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # ********************************* MORE ANALYTIC HACKING DETECTION) *********************************

        # Patch Level Status
        optional_analytical_detection = self.mobile_phone_hacking_detector_view_frame.add("Analytical Detecting")
        patch_level_status = customtkinter.CTkButton(optional_analytical_detection, text="Detect Patch-level",
                                                     state=status, command=detect_patch_level)
        patch_level_status.grid(row=1, column=3, padx=20, pady=(10, 10))

        # Boot state
        boot_state_status = customtkinter.CTkButton(optional_analytical_detection, text="Boot State Analysis",
                                                    state=status, command=boot_state_analysis)
        boot_state_status.grid(row=2, column=3, padx=20, pady=(10, 10))

        # SELinux Status
        SELinux_status = customtkinter.CTkButton(optional_analytical_detection, text="SELinux Analysis",
                                                 state=status, command=SELinux_analysis)
        SELinux_status.grid(row=3, column=3, padx=20, pady=(10, 10))

        # Rooted State Analysis
        root_state = customtkinter.CTkButton(optional_analytical_detection, text="isRooted Analysis",
                                             state=status, command=rooted_state)
        root_state.grid(row=4, column=3, padx=20, pady=(10, 10))

    # Then, you can use this method in your existing code:

    def login_state(self) -> str:
        return "enabled" if not self.login_status else "disabled"  # Controlled by login status

    def disconnect_button_status(self, status):
        self.disconnect_button.destroy()
        self.disconnect_button = customtkinter.CTkButton(self.sideBarFrame, text="Disconnect Device",
                                                         command=self.disconnect_device)
        self.disconnect_button.grid(row=2, column=0, padx=20, pady=20)
        self.disconnect_button.configure(state=status)

    def main_color_changer(self, int_random: int):
        #   int_random = int_val  # random.randint(0, 1)
        if int_random == 0:
            self.main_frame_color = "#00538E"  # Inactive color
        if int_random == 1:
            self.main_frame_color = "#6BD0FF"  # Active color
        if int_random == 2:
            self.main_frame_color = THEM[2]  # Green
        if int_random == 3:
            self.main_frame_color = THEM[1]  # Yellow
        if int_random == 4:
            self.main_frame_color = "#CC3300"  # Hacked color Red

    def object_state(self):
        return 'normal' if self.main_frame_color in ["#6BD0FF", "#CC3300"] else 'disabled'

    def connect_device(self):
        # You can replace the print statement with your connection code.
        start_adb_server()
        self.connection_progress_bar.start()  # Progress bar starts
        self.live_text = "Connection >>>"  # Insert text at the end of the textbox
        self.side_bar_text_box.insert(tk.END, f"\n{self.live_text}")

        port = get_port_name()  # Imported
        phone = Phone(port)
        option_vendor = None
        option_device = None

        phone_option = enumerate_serial_phones()
        for device in phone_option:
            option_vendor = device['Vendor ID']
            option_device = device['Product ID']
        if devices:
            connector = MobilePhoneLowLevelConnector(path, target_name=devices[0])
            create_phone_files_folder()  # Create a folder for the device if not exist
            connector.connect_phone_adb()
            self.general_textbox.insert(tk.END, connector.detect_device()[1] + f"@ Port {port}" + '\n')
            self.general_textbox.insert(tk.END, f"Vendor ID: {phone.return_vendor()} | {option_vendor} "
                                                f"Device ID: {phone.return_device()} | {option_device}\n")
        else:
            self.general_textbox.insert(tk.END, "No ADB device connected\n")
            return

        self.main_frame_color = "#6BD0FF"  # Active color
        self.disconnect_button_status("enabled")
        self.mobile_phone_graphics.destroy()
        self.mobile_phone_firmware_view_frame.destroy()
        self.mobile_phone_view_frame.destroy()
        self.mobile_phone_hacking_detector_view_frame.destroy()
        self.main_color_changer(1)
        self.phone('enabled')  # boot enabled tab
        self.firmware_hardware_analysis('enabled')  # boot enabled tab
        self.phone_hardware_firmware('enabled')
        self.firmware_hardware_hacking_detect('enabled')
        self.drop_down_menu.configure(state='enabled')
        self.execute_button.configure(state="enabled")
        self.pull_android_manifest_button.configure(state='enabled')
        self.connection_progress_bar.start()  # Progress bar stops
        self.app_drop_down_menu.configure(state='enabled')
        self.pull_app_memo_dump_dropdown.configure(state='enabled')

    def disconnect_device(self):
        # You can replace the print statement with your disconnection code.
        stop_adb_server()
        print("Device Disconnected")
        self.live_text = "Disconnection >>>"  # Insert text at the end of the textbox
        self.side_bar_text_box.insert(tk.END, f"\n{self.live_text}")
        self.connection_progress_bar.stop()  # Progress bar stops
        self.mobile_phone_graphics.destroy()
        self.main_color_changer(0)
        self.phone("disabled")
        self.disconnect_button_status("disabled")
        self.mobile_phone_firmware_view_frame.destroy()
        self.mobile_phone_view_frame.destroy()
        self.mobile_phone_hacking_detector_view_frame.destroy()
        self.firmware_hardware_analysis('disabled')
        self.phone_hardware_firmware('disabled')
        self.firmware_hardware_hacking_detect('disabled')
        self.drop_down_menu.configure(state='disabled')
        self.execute_button.configure(state="disabled")
        self.pull_android_manifest_button.configure(state="disabled")
        self.connection_progress_bar.stop()  # Progress bar stops
        self.app_drop_down_menu.configure(state='disabled')
        self.pull_app_memo_dump_dropdown.configure(state='disabled')

    def get_hardware_details(self):
        print("Hardware Loaded")
        host = os.path.join(immediate_dir, 'device_properties.txt')
        # h = Hardware(immediate_dir + "\\device_properties.txt")
        h = Hardware(host)
        self.hardware_text_box.insert(tk.END, extract_device_info(immediate_dir, 'device_properties.txt')[0] +
                                      '\n' + h.run() + '\n')

    def get_firmware(self):
        # print(detect_firmware_on_adb_device().split(',')[0])
        # self.firmware_text_box.insert(tk.END, detect_firmware_on_adb_device('{', '}').split(',')[0] + '\n')

        self.firmware_text_box.insert(tk.END, f"Pulled Firmware:"
                                              f"{get_firmware_version(immediate_dir, 'device_properties.txt')}\n")
        self.firmware_text_box.insert(tk.END, f"LIVE FIRMWARE: \n")
        self.firmware_text_box.insert(tk.END, {detect_firmware_on_adb_device()[0]})
        self.firmware_text_box.insert(tk.END, f"\n{detect_firmware_on_adb_device()[1]}")

    def analyseFirmware(self):  # TODO pass firmware: Firmware
        self.live_text = 'Analysis Begins ...'
        self.firmware_analysis_text_box.insert(tk.END, f"{self.live_text}\n")
        print(f"{COLOR[2]}This Firmware Analysis Begins{COLOR[4]}")
        f_analysis = FirmwareAnalyser(None)
        f_analysis_result = f_analysis.analyse(immediate_dir)
        self.firmware_analysis_text_box.insert(tk.END, f"PatchLevel: {f_analysis_result[0]}\nSelinux: "
                                                       f"{f_analysis_result[1]}\nBoot State: {f_analysis_result[2]}\n"
                                                       f"{f_analysis_result[3]}\n")
        self.general_textbox.insert(tk.END, f"***Analytical Detection***\nSecurity Patch Level {f_analysis_result[0]}\n"
                                            f"→The Bootloader, Kernel Not Tampered\nSELinux is ENFORCING --> ACTIV\n"
                                            f"Device No Rooted State Detected\n***Analytical Detection END***\n")
        self.live_text = 'Analysis ENDS'
        self.firmware_analysis_text_box.insert(tk.END, f"{self.live_text}\n")
        # Patch Level Computation Begins ....
        current_date = datetime.datetime.fromtimestamp(time.time()).date()
        patch_date = datetime.datetime.strptime(f_analysis_result[0], "%Y-%m-%d").date()
        time_difference = current_date - patch_date
        months_old = time_difference.days // 30  # Approximate months

        if f_analysis_result[1] == (1, 1) and f_analysis_result[2] == 'GREEN' and f_analysis_result[3] \
                == 'Root State OEM':
            self.main_frame_color = "#6BD0FF"  # Active color
            self.main_color_changer(2 if months_old <= 6 else 3)
            print(f"{COLOR[1]}Patch Level Passed{COLOR[4]}\n" if months_old <= 6 else
                  f"{COLOR[0]}Patch Level Failed!!{COLOR[4]}\n")
        else:
            self.main_frame_color = "#6BD0FF"  # Active color
            self.main_color_changer(4)
            # TODO **********************************************************************TODO
            print(f"{COLOR[0]}Check the Report to Determine Failed Property {COLOR[0]}")

        self.mobile_phone_graphics.destroy()
        self.phone('enabled')

        print(".....\n" * 2)
        print(f"{COLOR[1]}This Firmware Analysis is Complete, See the Report{COLOR[4]}")

    def analyseHardware(self):  # TODO hardware: Hardware
        print("Hardware Analysed")
        self.live_text = "Hardware Analysing"
        self.hardware_analysis_text_box.insert(tk.END, f"\n{self.live_text}")
        self.main_frame_color = "#6BD0FF"  # Active color
        self.mobile_phone_graphics.destroy()
        self.main_color_changer(4)
        self.phone('enabled')

    def detect_hack_firmware(self):
        print("Detecting Firmware Version")
        self.hacking_text_box.insert(tk.END, "Firmware Detecting>\n")

    def detect_hack_hardware(self):
        print("Hardware hack detection ran")
        self.hacking_text_box.insert(tk.END, "Hardware Detecting>\n")

    def monitor_system(self, system):
        pass

    def phone(self, status):
        # Mobile phone graphics
        self.initialize_tabview()  # Initial tab view elements
        self.mobile_phone_graphics = customtkinter.CTkTabview(self.root_ctk, width=250, state=status)
        self.mobile_phone_graphics.grid(row=1, column=3, padx=(20, 0), sticky="nsew")
        self.mobile_phone_graphics.grid_rowconfigure(4, weight=1)
        phone_demo = self.mobile_phone_graphics.add("Phone")
        flame_width = 100
        flame_height = 210
        phone_screen_graphics = customtkinter.CTkFrame(phone_demo, width=flame_width, height=flame_height,
                                                       fg_color=self.main_frame_color)

        # Pack it in the center of the tab
        # Pack it in the center top of the tab
        phone_screen_graphics.pack(expand=True, anchor="n")
        # self.mobile_phone_graphics.configure(state='enabled')

        # Create symbols for network and battery
        network_symbol = "📶"  # This can be replaced with an image for a more accurate representation
        battery_symbol = "🔋"  # This can be replaced with an image for a more accurate representation
        call_symbol = "📞"  # Telephone receiver
        mute_symbol = "🔇"  # Muted speaker
        key_up_symbol = "⬆"  # Upward-pointing arrow symbol
        return_symbol = "↩"

        '''Add network, battery, time and date at the top of the phone screen'''
        # Add network label in the top left corner of the frame
        network_label = customtkinter.CTkLabel(phone_screen_graphics, text=network_symbol,
                                               fg_color=self.main_frame_color,
                                               text_color='black', font=("Arial", 18))
        network_label.place(x=2, y=2, anchor="nw")

        # Add battery label in the top right corner of the frame
        battery_label = customtkinter.CTkLabel(phone_screen_graphics, text=battery_symbol,
                                               fg_color=self.main_frame_color,
                                               text_color='black', font=("Arial", 18))
        battery_label.place(x=flame_width - 2, y=flame_height - 208, anchor="ne")  # WAS 98

        '''Get current date and time'''
        # current_time = datetime.now().strftime("%H:%M") # *** works with from datetime import datetime
        current_time = datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M")
        # current_date = datetime.now().strftime("%Y-%m-%d") # *** works with from datetime import datetime
        current_date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
        current_time_label = customtkinter.CTkLabel(phone_screen_graphics, text=current_time,
                                                    fg_color=self.main_frame_color, text_color='black',
                                                    font=("Arial", 18))
        x__ = (flame_width / 2.0)  # WAS 2
        # y__ = (flame_height / 2) + 10
        y__ = (16.0 / 21.0) * flame_height
        current_time_label.place(x=flame_width - x__, y=flame_height - y__, anchor="center")
        '''Get current date and time'''
        current_date_label = customtkinter.CTkLabel(phone_screen_graphics, text=current_date,
                                                    fg_color=self.main_frame_color,
                                                    text_color='black',
                                                    font=("Arial", 12))
        _y = 40  # (flame_height / 2) - 10  # WAS 2
        _y = (16.0 / 21.0) * flame_height - 20
        current_date_label.place(x=flame_width - x__, y=flame_height - _y, anchor="center")

        # Call Button *********************
        call_button = customtkinter.CTkLabel(phone_screen_graphics, text=call_symbol, text_color='white', height=21,
                                             width=21, font=("Arial", 16), bg_color='#000033')
        call_button.place(x=flame_width - x__, y=flame_height - 115, anchor="center")  # WAS 15

        # Disable all child widgets within the frame
        button_bg_state = ''
        for child in phone_screen_graphics.winfo_children():
            if self.main_frame_color == "#6BD0FF" or self.main_frame_color == "#CC3300":
                child.configure(state="normal")
                button_bg_state = 'normal'
            else:  # self.main_frame_color == "#00538E":
                child.configure(state="disabled")
                button_bg_state = 'disabled'

        """ Place buttons in the phone graphics"""

        row = flame_width - 98.0
        col = flame_height - 90.0
        x_ = 0.0

        one_7 = []
        for i in range(1, 10):
            one_7.append(i)
        for i in range(8):  # Increase the range for placing four buttons
            btn = customtkinter.CTkButton(phone_screen_graphics, text=f"{one_7[i]}", width=2, height=1,
                                          text_color='#F9E79F', fg_color='#2d2766', state=button_bg_state,
                                          font=("Arial", 10), command=None)
            btn.place(x=row + x_, y=col)
            x_ += 14.0  # Increment x_ for horizontal spacing between buttons

        '''Generate some qwerty keyboard by abstracting a QWERTY keyboard layout'''
        lower = list(string.ascii_lowercase)
        lowercase_alphabets = [
            lower[16], lower[22], lower[4], lower[17], key_up_symbol, lower[19], lower[24], lower[20], lower[8],
            lower[14], return_symbol, lower[15], lower[0], lower[18], lower[3], lower[5], lower[6], lower[7], lower[9],
            lower[10], '#', lower[11], lower[25], lower[23], lower[2], lower[21], lower[1], lower[13], lower[12]
        ]

        eight_zero = [8, 9, 0] + lowercase_alphabets
        x_ = 0.0
        for i in range(8):  # Increase the range for placing four buttons
            btn = customtkinter.CTkButton(phone_screen_graphics, text=f"{eight_zero[i]}", width=2, height=1,
                                          text_color='#F9E79F', fg_color='#2d2766', state=button_bg_state,
                                          font=("Arial", 10), command=None)
            btn.place(x=row + x_, y=col + 22.0)
            x_ += 14.0  # Increment x_ for horizontal spacing between buttons

        x_ = 0.0
        start_index = lowercase_alphabets.index(key_up_symbol)
        lowercase_alphabets = lowercase_alphabets[start_index:] + lowercase_alphabets[:start_index]
        for i in range(7):  # Increase the range to 4 for placing four buttons
            btn = customtkinter.CTkButton(phone_screen_graphics, text=f"{lowercase_alphabets[i]}", width=2, height=1,
                                          text_color='#F9E79F', fg_color='#2d2766', state=button_bg_state,
                                          font=("Arial", 10), command=None)
            btn.place(x=(row - 1.0) + x_, y=col + 44.0)
            x_ += 14  # Increment x_ for horizontal spacing between buttons

        x_ = 0.0
        start_index = lowercase_alphabets.index('#')
        lowercase_alphabets = lowercase_alphabets[start_index:] + lowercase_alphabets[:start_index]
        for i in range(7):  # Increase the range for placing four buttons
            btn = customtkinter.CTkButton(phone_screen_graphics, text=f"{lowercase_alphabets[i]}", width=2, height=1,
                                          text_color='#F9E79F', fg_color='#2d2766', state=button_bg_state,
                                          font=("Arial", 10), command=None)
            btn.place(x=(row - 1.0) + x_, y=col + 66.0)
            x_ += 14.0  # Increment x_ by horizontal spacing between buttons

    def initialize_tabview(self):
        self.root_ctk.grid_rowconfigure(0, weight=1)
        self.root_ctk.grid_columnconfigure(1, weight=1)

    @property
    def create_help_menu_html(self):
        help_menu_text = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    .green { color: green; }
                    .red { color: red; }
                    .blue { color: blue; }
                    .grey { color: grey; }
                    .black { color: black; }
                    table {
                        border-collapse: collapse;
                        width: 60%;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
            <h2 style="color: blue;">Detecting Mobile Phone Firmware Hardware Hacking</h2>
            <h2 style="color: red;"> -------------------User Menu--------------------</h2>
        
            <h2>User Interface (GUI)</h2>
            <table>
                <tr>
                    <th class="green">GUI Commands</th>
                    <th class="green">Description</th>
                </tr>
                <tr>
                    <td class="red">Them Switching</td>
                    <td class="red">Change Theme to Dark, Light & System Defaulted.</td>
                </tr>
                <!-- Add more rows for other commands here -->
            </table>
        
            <h2>System Commands </h2>
            <table>
                <tr>
                    <th class="green">User Commands</th>
                    <th class="green">Description</th>
                </tr>
                <tr>
                    <td class="red">Connect Phone <strong>-- BUTTON</strong></td>
                    <td class="red">>>> Click to connect Phone</td>
                </tr>
                <tr>
                    <td class="grey"> Pull File <strong>--ITEMS_STORE</strong></td>
                    <td class="grey"> Pull Selected File </td>
                </tr>
                <tr>
                    <td class="red"> Drop Down for Files <strong>COMBO_BOX</strong></td>
                    <td class="red"> Drop Down Selection Apps </td>
                </tr>
                <tr>
                    <td class="red"> Pull File <strong>-- BUTTON</strong></td>
                    <td class="red"> Pull Selected file </td>
                </tr>
                <tr>
                    <td class="red"> Pull App AndroidManifest.xml <strong>-- BUTTON</strong></td>
                    <td class="red"> Pull App Android Manifest </td>
                </tr>
                <tr>
                    <td class="red">--------------</td>
                    <td class="red">------------------</td>
                </tr>
                <tr>
                    <td class="grey">Malware Detection <strong>ITEMS_STORE</strong></td>
                    <td class="grey">Malicious Apps Detection House </td>
                </tr>
                <tr>
                    <td class="blue"><strong> Select Model COMBO_BOX<strong></td>
                    <td class="blue"><strong> !Select ML Model for Analysis/Prediction</strong></td>
                </tr>
                <tr>
                    <td class="red">Analyse Saved APK <strong>-- BUTTON</strong></td>
                    <td class="red">Scan Immidiate App to Detect If Malicious </td>
                </tr>
                <tr>
                    <td class="red"> Drop Down Select App To Scan <strong>-- COMBO_BOX<strong></td>
                    <td class="red"> Here you Chose App To Scan Using ML </strong></td>
                </tr>
                <tr>
                    <td class="red"> Scan App <strong>-- BUTTON</strong></td>
                    <td class="red">>>>Scan App Selected and Wait for Results<br>>>>.jason Stats Report is Now Saved </td>
                </tr>
                <tr>
                    <td class="red"> Scan All App <strong>-- BUTTON</strong></td>
                    <td class="red">>>>Select All Apps Scan All & Wait for Results<br>>>>All.jason Stats Report is Now Saved </td>
                </tr>
                <tr>
                    <td class="grey">Mobile Hardware <strong>ITEMS_STORE</strong></td>
                    <td class="grey">Mobile Phone Hardware Properties House </td>
                </tr>
                <tr>
                    <td class="red"> Phone Hardware Detect <strong>-- BUTTON</strong></td>
                    <td class="red">>>>Detect Phone Key Hardware Components</td>
                </tr>
                <tr>
                    <td class="grey">Mobile Firmware <strong>ITEMS_STORE</strong></td>
                    <td class="grey">Mobile Phone Firmware Properties House </td>
                </tr>
                <tr>
                    <td class="red"> Phone Firmware Detect <strong>-- BUTTON</strong></td>
                    <td class="red">>>>Detect Phone Firmware Properties</td>
                </tr>
                <tr>
                    <td class="grey">Firmware Analysis  <strong>ITEMS_STORE</strong></td>
                    <td class="grey">Mobile Phone Firmware Analysis House </td>
                </tr>
                <tr>
                    <td class="red">Firmware Analyser<strong>-- BUTTON</strong></td>
                    <td class="red">Analyse Phone Firmware Will Dectect<br> >>> Patch-level<br>>>> Boot State<br>>>> 
                    SELinux<br>>>> isRooted State</td>
                </tr>
                <tr>
                    <td class="grey">Hardware Analysis  <strong>ITEMS_STORE</strong></td>
                    <td class="grey">Mobile Phone Hardware Analysis House </td>
                </tr>
                <tr>
                    <td class="red"> Hardware Analysis <strong>-- BUTTON</strong></td>
                    <td class="red">>>>Analyse Phone Firmware Will Dectect</td>
                </tr>
                <tr>
                    <td class="grey">Detect Hacking  <strong>ITEMS_STORE</strong></td>
                    <td class="grey">Hacking Detector House </td>
                </tr>
                <tr>
                    <td class="red"> Detect Hardware Hacking<strong>-- BUTTON</strong></td>
                    <td class="red">>>>Detect if Phone Hardware Has Been Compromised</td>
                </tr>
                <tr>
                    <td class="red"> Detect Firmware Hacking <strong>-- BUTTON</strong></td>
                    <td class="red">>>>Detect if Phone Firmware Has Been Compromised</td>
                </tr>
                <tr>
                    <td class="grey">Analytical Detecting  <strong>ITEMS_STORE</strong></td>
                    <td class="grey">Analysitic Detection House </td>
                </tr>
                <tr>
                    <td class="red"> Detect Patch-level <strong>-- BUTTON</strong></td>
                    <td class="red">>>>This Detects Patch Level Installed</td>
                </tr>
                <tr>
                    <td class="red"> Boot State Analysis <strong>-- BUTTON</strong></td>
                    <td class="red">>>>This Detects if Boot State Has Changed</td>
                </tr>
                <tr>
                    <td class="red"> SELinux Analysis <strong>-- BUTTON</strong></td>
                    <td class="red">>>>This Detects if SELinux State has Been Modified </td>
                </tr>
                <tr>
                    <td class="red"> isRooted Analysis <strong>-- BUTTON</strong></td>
                    <td class="red">>>>This Detects if Phone has Been Roots !Serious Vulunable State</td>
                </tr>
                <!-- Add rows for ADB options here -->
            </table>
        
            <h2>Results</h2>
            <table>
                <tr>
                    <th class="green">Outcomes</th>
                    <th class="green">Description</th>
                </tr>
                <tr>
                    <td class="red">Phone COLOR = LIGHT_BLUE</td>
                    <td class="red">Indicates Phone Successfully Connected in Developer Mode</td>
                </tr>
        
                <!-- Add more rows for other commands here -->
            </table>
        
            </body>
            </html>
        """
        return help_menu_text

    def save_and_read_help_menu_html(self, folder_path='doc'):
        try:
            # Create the folder if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)

            # Define the full path for the HTML file
            html_file_path = os.path.join(folder_path, 'help.html')

            # Generate the HTML content

            # Check if the HTML file already exists
            if not os.path.exists(html_file_path):
                # Generate the HTML content
                help_menu_html = self.create_help_menu_html

                # Save the HTML content to the file
                with open(html_file_path, 'x') as file:
                    file.write(help_menu_html)

                print(f"Help HTML Generated Saved in {html_file_path}")
            else:
                print(f"Help HTML Opened")

            # Open the HTML file in a web browser
            import webbrowser
            webbrowser.open(html_file_path)

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    run = SystemUserInterface()
    run.root_ctk.mainloop()
