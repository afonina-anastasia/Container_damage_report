import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import re


def modify_pdf():
    code = entry_code.get()
    code_info = get_code_info(code)

    if code_info != "Such code does not exist.":
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont(
            "Helvetica-Bold", 10
        )
        can.drawString(50, 332, f" {code_info}")
        can.save()
        packet.seek(0)

        existing_pdf = PdfReader(open("DC.pdf", "rb"))
        output = PdfWriter()

        page = existing_pdf.pages[0]

        target_word = "Remarks"
        text = page.extract_text()
        match = re.search(r"\b{}\b".format(re.escape(target_word)), text)
        if match:
            start_index = match.start()
            end_index = match.end()

            new_pdf = PdfReader(packet)
            new_page = new_pdf.pages[0]

            page.merge_page(new_page)
            output.add_page(page)

            with open("Newfile.pdf", "wb") as outputStream:
                output.write(outputStream)
        else:
            print("Target word not found in the document.")

    text_output.delete("1.0", tk.END)
    text_output.insert("1.0", code_info)


def clear():
    entry_code.delete(0, tk.END)
    text_output.delete("1.0", tk.END)


def get_code_info(code):

    codes_meaning = {
        "00": "FRONT SIDE – TOP RAIL DAMAGE",
        "01": "FRONT SIDE – BOTTOM RAIL DAMAGE",
        "02": "FRONT SIDE – HOLE/TEAR/CUT",
        "03": "FRONT SIDE – OUT OF STANDARD/DAMAGED",
        "04": "FRONT SIDE – PUSH IN/OUT",
        "05": "FRONT SIDE – DENTED/SCRATCHED",
        "10": "REAR SIDE – TOP RAIL DAMAGE",
        "11": "REAR SIDE – BOTTOM RAIL DAMAGE",
        "12": "REAR SIDE – HOLE/TEAR/CUT",
        "13": "REAR SIDE – OUT OF STANDARD/DAMAGED",
        "14": "REAR SIDE – PUSH IN/OUT",
        "15": "REAR SIDE – DOORS NOT COMPLETELY LOCKED",
        "16": "REAR SIDE – LOCKING/HANDLE BAR BENT/BROKEN",
        "17": "REAR SIDE – HINGES DAMAGED",
        "18": "REAR SIDE – DENTED/SCRATCHED",
        "19": "REAR SIDE – GASKET DAMAGED/MISSING",
        "20": "LEFT SIDE – TOP RAIL DAMAGE",
        "21": "LEFT SIDE – BOTTOM RAIL DAMAGE",
        "22": "LEFT SIDE – HOLE/TEAR/CUT",
        "23": "LEFT SIDE – OUT OF STANDARD/DAMAGED",
        "24": "LEFT SIDE – CORNER POST DAMAGE",
        "25": "LEFT SIDE – CORNER FITTINGS DAMAGE",
        "26": "LEFT SIDE – PUSH IN/OUT",
        "27": "LEFT SIDE – DENTED/SCRATCHED",
        "30": "RIGHT SIDE – TOP RAIL DAMAGE",
        "31": "RIGHT SIDE – BOTTOM RAIL DAMAGE",
        "32": "RIGHT SIDE – HOLE/TEAR/CUT",
        "33": "RIGHT SIDE – OUT OF STANDARD/DAMAGED",
        "34": "RIGHT SIDE – CORNER POST DAMAGE",
        "35": "RIGHT SIDE – CORNER FITTINGS DAMAGE",
        "36": "RIGHT SIDE – PUSH IN/OUT",
        "37": "RIGHT SIDE – DENTED/SCRATCHED",
        "50": "ROOF – TARPUALIN DAMAGED",
        "51": "ROOF – TARPAULIN MISSING",
        "52": "ROOF – TARPAULIN NOT ATTACHED",
        "53": "ROOF – TIEROPE DAMAGED",
        "54": "ROOF – TIEROPE MISSING",
        "55": "ROOF – HOLE/TEAR/CUT",
        "56": "ROOF – OUT OF STANDARD/DAMAGED",
        "57": "ROOF – PUSH IN/OUT",
        "58": "ROOF – DENTED/SCRATCHED",
        "60": "INTERIOR – DIRTY/STINKING",
        "61": "INTERIOR – WET FLOOR",
        "62": "INTERIOR – ROOF BOWS/SUPPORT DAMAGED/MISSING",
        "63": "INTERIOR – SIDE PANELS DAMAGED/MISSING",
        "64": "INTERIOR – FLOOR DAMAGED",
        "70": "TANK – TANK SHELL DAMAGED",
        "71": "TANK – FRAME DAMAGED",
        "72": "TANK – TANK VALVES/PIPES DAMAGED",
        "73": "TANK – TANK PANELS DAMAGED",
        "80": "REEFER – CABLE MISSING",
        "81": "REEFER – CABLE DAMAGED",
        "82": "REEFER – AIR VENT OPEN",
        "83": "REEFER – AIR VENT DAMAGED",
        "84": "REEFER – REEFER PLUG MISSING",
        "85": "REEFER – REEFER PLUG DAMAGED",
        "86": "REEFER – GENERATOR SYSTEM/PANEL DAMAGED",
        "90": "GENERAL – LABELS MISSING",
        "91": "GENERAL – OLD LABELS NOT REMOVED",
        "92": "GENERAL – NOT SEALED UPON ARRIVAL TO TERMINAL",
        "93": "GENERAL – CONTAINER LEAKING",
        "94": "GENERAL – DENTED ON SEVERAL PLACES",
        "95": "GENERAL – CONTAINER BURNED",
        "96": "GENERAL – OUT OF SERVICE",
        "97": "GENERAL – VENTILATORS DAMAGED",
        "98": "GENERAL – CROSS MEMBER DAMAGED",
        "99": "CONTAINER IN GOOD CONDITION",
    }

    if code in codes_meaning:
        return codes_meaning[code]
    else:
        return "Such code does not exist."


win = tk.Tk()
win.title("Container Damage Code")

label = tk.Label(win, text="Enter the damage code:")
label.pack()

entry_code = tk.Entry(win)
entry_code.pack()

button_info = tk.Button(win, text="Get Information", command=modify_pdf)
button_info.pack()

text_output = ScrolledText(win, height=10, width=50, font=("Arial", 12))
text_output.pack()

button_clear = tk.Button(win, text="Clear", command=clear)
button_clear.pack()


win.mainloop()
