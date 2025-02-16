import tkinter as tk # Used for building the GUI
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD # Drag and drop
from PIL import Image # Resizing images
from fpdf import FPDF # Generate PDFs
from fpdf.enums import XPos, YPos # Position text in the PDF
from datetime import datetime # Timestamp generation

# The main application class
class CablewayInspectionApp:

    # Constructor
    def __init__(self, root):
        self.root = root
        # Window title
        self.root.title("Cableway Inspection Report")
        # Window size
        self.root.geometry("500x550")

        # List of images to eventually store
        self.images = []

        # Calls helper functions
        self.create_form()
        self.create_image_upload_area()
        self.create_generate_button()

    # Creates the scrollable form where the user can input inspection data
    def create_form(self):
        # Creates the overall window frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=5)

        # Creates a canvas for scrolling (This is the section where all data will be inputted)
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

        # This canvas will be scrollable
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # Links the scrollbar to the previously defined canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # The space for the inspection data that will be inputted by the user
        self.fields = {}
        self.fields_cable = {}
        # All the inspection data necessary for the report
        form_fields = ["Station Name", "Station Number", "Inspector Name", "Reviewer Name", "Date Inspected", "Weather Conditions", "Temperature (°C)", "Span (m)", "Sag (m)", "Design Load (kg)", "Recommendations"]
        form_fields_cable = ["Diameter (in)", "Angle from Vertical (deg)", "Cable Type", "Core Type", "Broken Wires", "Pinched Wires", "Broken Strands", "Frays", "Rust", "Distortion", "Chainage Marks", "Comments"]

        # Add a note that says that the following data inputted is for general.
        general_label = ttk.Label(self.scrollable_frame, text="General Data:", font=("Arial", 10, "bold"))
        general_label.pack(pady=(10, 5))

        # For loop for iterating through all the inspection parameters in form_fields
        for field in form_fields:
            # Creates a horizontal frame for the name and an input box
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, padx=5, pady=5)
            # Creates a label for the data
            label = ttk.Label(frame, text=field)
            label.pack(side=tk.LEFT)
            # Textbox for "Recommendations" is larger than the other fields
            entry = ttk.Entry(frame, width=40)
            # Adds the input field to the frame and stores it in self.fields
            entry.pack(side=tk.LEFT, padx=5)
            self.fields[field] = entry

        # Add a note that says that the following data inputted is for cable.
        cable_label = ttk.Label(self.scrollable_frame, text="Cable Data:", font=("Arial", 10, "bold"))
        cable_label.pack(pady=(10, 5))

        # For loop for iterating through all the inspection parameters in form_fields_cable
        for field in form_fields_cable:
            # Creates a horizontal frame for the name and an input box
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, padx=5, pady=5)
            # Creates a label for the data
            label = ttk.Label(frame, text=field)
            label.pack(side=tk.LEFT)
            # Textbox for "Recommendations" is larger than the other fields
            entry = ttk.Entry(frame, width=40)
            # Adds the input field to the frame and stores it in self.fields
            entry.pack(side=tk.LEFT, padx=5)
            self.fields_cable[field] = entry

        # Positions the canvas and the scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Creates image upload area with a drag and drop (dnd) interface
    def create_image_upload_area(self):
        # Creates the frame for the image upload area
        frame = ttk.LabelFrame(self.root, text="Image Upload")
        frame.pack(fill=tk.X, padx=10, pady=5)

        # Labels that this area is for dnd
        self.drop_area = ttk.Label(frame, text="Drag and drop images here or click Browse", padding=50)
        self.drop_area.pack(fill=tk.X)
        # Registers the drop area to accept file drops.
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.handle_drop)

        # A button for uploading photos manually
        browse_btn = ttk.Button(frame, text="Browse", command=self.browse_files)
        browse_btn.pack(pady=5)
        # Shows how many images have been uploaded
        self.image_count = ttk.Label(frame, text="Images: 0")
        self.image_count.pack()

    # Creates the button for generating the pdf
    def create_generate_button(self):
        # Calls the "self.generate_report() function when clicked"
        generate_btn = ttk.Button(self.root, text="Generate Report", command=self.generate_report)
        generate_btn.pack(pady=10)

    # Handles the dnd photos
    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        self.process_image_files(files)

    # Handles the manually uploaded photos (up to multiple at once)
    def browse_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        self.process_image_files(files)

    # Processes the images
    def process_image_files(self, files):
        for file in files:
            # If the images are of valid input (chose png, jpg, and jpeg), then add them to self.images
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.images.append(file)
        # Increment the image count
        self.image_count.config(text=f"Images: {len(self.images)}")

    # Collects the inputted data
    def get_form_data(self):
        data = {}

        # Loops through each form field taking the data
        for field, entry in self.fields.items():
            if isinstance(entry, tk.Text):
                data[field] = entry.get("1.0", tk.END).strip()
            else:
                data[field] = entry.get().strip()

        for field, entry in self.fields_cable.items():
            if isinstance(entry, tk.Text):
                data[field] = entry.get("1.0", tk.END).strip()
            else:
                data[field] = entry.get().strip()


        # Returns the collected data as a dictionary
        return data



    # Saves and creates the pdf
    def generate_report(self):
        data = self.get_form_data()
        # Get the current time
        date_str = datetime.now().strftime("%B %d, %Y")
        filename_date = datetime.now().strftime("%Y-%m-%d")
        # Generate the file name: Cableway_Inspection_YYYYMMDD_StationName_StationNumber.pdf
        filename = f"Cableway_Inspection_{filename_date}_{data.get('Station Name', '')}_{data.get('Station Number', '')}.pdf"

        # Creates a new FPDF object, sets the margins, and creates the first page
        pdf = FPDF()
        pdf.set_margins(20, 20, 20)
        pdf.add_page()

        # Sets the font, and creates the title
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "Cableway Inspection Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(5)

        # Includes a section where the station name and number are displayed
        pdf.set_font("helvetica", "", 10)
        pdf.cell(0, 8, f"Station Name: {data.get('Station Name', '')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.cell(0, 8, f"Station Number: {data.get('Station Number', '')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.cell(0, 8, f"Inspection Date: {data.get('Date Inspected', '')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(5)

        # Table title
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "General Information:", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

        excluded_fields = ["Station Name", "Station Number", "Inspector Name", "Reviewer Name", "Date Inspected", "Diameter (in)", "Angle from Vertical (deg)", "Cable Type", "Core Type", "Broken Wires", "Pinched Wires", "Broken Strands", "Frays", "Rust", "Distortion", "Chainage Marks", "Comments"]

        # Set font size for the table content
        pdf.set_font("helvetica", "", 12)

        # Set column widths
        col_width = 80
        row_height = 10

        # Iterate through all the form fields and print the inputted data in a table format
        for field, value in data.items():
            if field not in excluded_fields:
                # Title is bold
                pdf.set_font("helvetica", "B", 12)
                pdf.cell(col_width, row_height, f"{field}:", border=1)

                # Data is not bold
                pdf.set_font("helvetica", "", 12)

                # Use cell for other fields
                pdf.cell(col_width, row_height, value, border=1)

                pdf.ln(row_height)


        pdf.ln(10)

        # Table title
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "Cable Information:", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")


        excluded_fields2 = ["Station Name", "Station Number", "Inspector Name", "Reviewer Name", "Date Inspected", "Weather Conditions", "Temperature (°C)", "Span (m)", "Sag (m)", "Design Load (kg)", "Recommendations"]

        # Set font size for the table content
        pdf.set_font("helvetica", "", 10)

        # Set column widths
        col_width = 80
        row_height = 10

        # Iterate through all the form fields and print the inputted data in a table format
        for field, value in data.items():
            if field not in excluded_fields2:
                # Title is bold
                pdf.set_font("helvetica", "B", 12)
                pdf.cell(col_width, row_height, f"{field}:", border=1)

                # Data is not bold
                pdf.set_font("helvetica", "", 12)

                # Use cell for other fields
                pdf.cell(col_width, row_height, value, border=1)

                pdf.ln(row_height)


        # If there are images, create a new page for them
        if self.images:
            pdf.add_page()
            pdf.set_font("helvetica", "B", 14)
            pdf.cell(0, 10, "Station Images", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

            # Image layout
            img_width, img_height, x_spacing, y_spacing = 50, 40, 60, 50
            x_start, y_start = 20, 40

            # Loops through all uploaded image file paths
            for i, img_path in enumerate(self.images):
                x = x_start + (i % 3) * x_spacing
                y = y_start + (i // 3) * y_spacing
                # If the image exceeds the page size, add a new page
                if y + img_height > pdf.h - 20:
                    pdf.add_page()
                    y_start = 40
                    y = y_start + ((i % 6) // 3) * y_spacing
                try:
                    pdf.image(img_path, x, y, img_width, img_height)
                except:
                    pass


        pdf.add_page()

        excluded_fields2 = ["Station Name", "Station Number", "Weather Conditions", "Temperature (°C)", "Span (m)", "Sag (m)", "Design Load (kg)", "Recommendations", "Diameter (in)", "Angle from Vertical (deg)", "Cable Type", "Core Type", "Broken Wires", "Pinched Wires", "Broken Strands", "Frays", "Rust", "Distortion", "Chainage Marks", "Comments", "Date Inspected"]

        # Reduce font size for the data
        pdf.set_font("helvetica", "", 12)
        # Iterate through all the form fields and prints the inputted data
        for field, value in data.items():
            if field not in excluded_fields2:
                # Title is bold
                pdf.set_font("helvetica", "B", 12)
                pdf.cell(60, 10, f"{field}:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                # Data is not bold
                pdf.set_font("helvetica", "B", 12)
                pdf.multi_cell(0, 8, value)
                pdf.ln(2)

        pdf.set_font("helvetica", "B", 12)
        pdf.cell(60, 10, f"Review Date: {date_str}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


# Saves the finalized pdf as the generated filename
        pdf.output(filename)
        # Message that confirms the generated pdf
        messagebox.showinfo("Success", f"Report saved as {filename}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = CablewayInspectionApp(root)
    root.mainloop()
