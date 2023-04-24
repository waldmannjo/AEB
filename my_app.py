# GUI to read files, process them (embedding) and the ask questions which are answered through chatGPT

import tkinter as tk
from tkinter import filedialog, simpledialog
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

import PyPDF2
import csv

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Processor")
        self.file_path = None
        
        # create button to select file
        select_file_button = tk.Button(root, text="Select File", command=self.select_file)
        select_file_button.pack(pady=10)
        
        # create button to process the document
        run_method_button = tk.Button(root, text="Process document", command=self.run_method)
        run_method_button.pack(pady=10)
        


        # create label for question field
        self.question_label = tk.Label(root, text="Enter a question:")
        self.question_label.pack()

        # create question field
        self.question_field = tk.Entry(root)
        self.question_field.pack(padx=10)
        
        # create button to send input result
        send_button = tk.Button(root, text="Send", command=self.send_input_result)
        send_button.pack(pady=10)
        
        # create label for the answer
        self.answer_label = tk.Label(root, text="")
        self.answer_label.pack(pady=10)
        
    def select_file(self):
        # open file dialog to select file
        filetypes = [("PDF files", "*.pdf"), ("Text files", "*.txt"), ("CSV files", "*.csv")]
        self.file_path = filedialog.askopenfilename(filetypes=filetypes)
    
    def run_method(self):
        if self.file_path is None:
            # show error message if no file is selected
            tk.messagebox.showerror("Error", "Please select a file first")
            return
        
        # determine file type and run corresponding method
        if self.file_path.endswith(".pdf"):
            # Open the PDF file in read-binary mode
            with open(self.file_path, 'rb') as file:
                # Create a PyPDF2 PdfFileReader object
                reader = PyPDF2.PdfReader(file)

                # Read the text from each page and append it to the raw_text variable
                self.raw_text = ''
                for i in range(len(reader.pages)):
                    page = reader.pages[i]
                    text = page.extract_text()
                    if text:
                        self.raw_text += text
            # pdf_file = open(self.file_path, "rb")
            # pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            # self.input_result = "Number of Pages: " + str(pdf_reader.numPages)
            # pdf_file.close()
        elif self.file_path.endswith(".txt"):
            self.raw_text = ''
            # Open the txt file in read mode
            with open(self.file_path, 'r') as file:
                # Read the text from the file and store it in the raw_text variable
                self.raw_text = file.read()  
            # text_file = open(self.file_path, "r")
            # self.input_result = "Number of Lines: " + str(len(text_file.readlines()))
            # text_file.close()
        elif self.file_path.endswith(".csv"):
            # open the CSV file specified by self.file_path
            with open(self.file_path, 'r') as file:
                # create a CSV reader object
                reader = csv.DictReader(file)
                
                # iterate over the rows in the CSV file and store them in a list
                rows = []
                for row in reader:
                    rows.append(row)

            # csv_file = open(self.file_path, "r")
            # csv_reader = csv.reader(csv_file)
            # num_rows = sum(1 for row in csv_reader)
            # self.input_result = "Number of Rows: " + str(num_rows)
            # csv_file.close()
        
        # update input result label with result
        self.input_result_label.config(text=self.raw_text)
        
    def send_input_result(self):
        if not self.input_result:
            # show error message if no input result is available
            tk.messagebox.showerror("Error", "Please run a method first")
            return
        
        # show input dialog to send input result
        input_text = simpledialog.askstring("Input Result", "Please enter input result:", initialvalue=self.input_result)
        if input_text:
            # do something with input text
            print("Input Result:", input_text)

from dotenv import load_dotenv
load_dotenv()

# create Tkinter window and run application
root = tk.Tk()
app = MyApp(root)
root.mainloop()
