import tkinter as tk
from tkinter import filedialog, messagebox
from inference_sdk import InferenceHTTPClient
import requests
from PIL import Image, ImageTk
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def process_image(image_path):
    client = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key=os.getenv("API_KEY")
    )

    try:
        result = client.run_workflow(
            workspace_name=os.getenv("WORKSPACE_NAME"),
            workflow_id=os.getenv("WORKFLOW_ID"),
            images={"image": image_path},
            use_cache=False  # Disabled caching to see workflow changes immediately
        )
        
        output = result[0] if result else {}
        
        # Load visualization image (base64 or URL)
        vis_img = None
        vis_data = output.get("label_visualization")
        if vis_data:
            if isinstance(vis_data, str) and vis_data.startswith("data:image"):
                base64_string = vis_data.split(",")[1] if "," in vis_data else vis_data
                img_data = base64.b64decode(base64_string)
                vis_img = Image.open(BytesIO(img_data))
            elif isinstance(vis_data, str) and (vis_data.startswith("/9j/") or vis_data.startswith("iVBOR")):
                img_data = base64.b64decode(vis_data)
                vis_img = Image.open(BytesIO(img_data))
            elif isinstance(vis_data, str) and vis_data.startswith("http"):
                response = requests.get(vis_data, timeout=10)
                response.raise_for_status()
                vis_img = Image.open(BytesIO(response.content))
        
        # Save visualization image
        if vis_img:
            vis_img.save("visualization_output.png")
        
        # Get inspection result and predictions
        inspection_result = output.get("inspection_result_json_output", "No inspection result available")
        predictions = output.get("model_predictions", {}).get("predictions", [])
        
        # Analyze predictions for majority class
        majority_class = "None"
        class_counts = {}
        if predictions:
            for pred in predictions:
                class_name = pred.get('class', 'Unknown')
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
            majority_class = max(class_counts, key=class_counts.get) if class_counts else "None"
        
        return {
            'vis_img': vis_img,
            'inspection_result': inspection_result,
            'predictions': predictions,
            'majority_class': majority_class,
            'class_counts': class_counts,
            'raw_output': output
        }
    
    except Exception as e:
        print(f"Error in process_image: {e}")
        return {
            'vis_img': None,
            'inspection_result': f"Error: {str(e)}",
            'predictions': [],
            'majority_class': "Error",
            'class_counts': {},
            'raw_output': {}
        }

class PCBInspectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PCB Defect Inspection")
        
        # Get screen dimensions and center window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = min(1200, int(screen_width * 0.8))
        window_height = min(900, int(screen_height * 0.8))
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.root.configure(bg="#1E2A44")
        
        # Font styles - responsive to screen size
        base_font_size = max(10, min(16, int(screen_width / 100)))
        self.header_font = ("Segoe UI", base_font_size + 6, "bold")
        self.label_font = ("Segoe UI", base_font_size)
        self.button_font = ("Segoe UI", base_font_size, "bold")
        self.text_font = ("Segoe UI", base_font_size - 2)
        
        # Colors
        self.bg_color = "#1E2A44"
        self.accent_color = "#00C4B4"
        self.secondary_color = "#FF6F61"
        self.text_color = "#FFFFFF"
        self.frame_color = "#2A3B5A"
        
        # Create main canvas with scrollbar
        main_canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        main_scrollbar = tk.Scrollbar(
            self.root,
            orient=tk.VERTICAL,
            command=main_canvas.yview,
            bg=self.bg_color,
            troughcolor=self.frame_color,
            highlightthickness=0
        )
        scrollable_frame = tk.Frame(main_canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        main_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Main container frame - centered
        container_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        container_frame.pack(expand=True, fill=tk.BOTH)
        
        # Main frame - all content goes here, centered
        main_frame = tk.Frame(container_frame, bg=self.bg_color)
        main_frame.pack(expand=True, anchor=tk.CENTER, padx=20, pady=20)
        
        # Header - centered
        header_label = tk.Label(
            main_frame,
            text="PCB Defect Inspection",
            font=self.header_font,
            fg=self.text_color,
            bg=self.bg_color
        )
        header_label.pack(pady=(0, 30))
        
        # Button frame - centered
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        # Select image button
        self.select_btn = tk.Button(
            button_frame,
            text="Select Image",
            command=self.select_image,
            font=self.button_font,
            bg=self.accent_color,
            fg=self.text_color,
            activebackground="#00A69A",
            activeforeground=self.text_color,
            bd=0,
            relief=tk.FLAT,
            padx=30,
            pady=15
        )
        self.select_btn.pack(side=tk.LEFT, padx=15)
        self.select_btn.bind("<Enter>", lambda e: self.select_btn.config(bg="#00A69A"))
        self.select_btn.bind("<Leave>", lambda e: self.select_btn.config(bg=self.accent_color))
        
        # Process button
        self.process_btn = tk.Button(
            button_frame,
            text="Process Image",
            command=self.process_image,
            font=self.button_font,
            bg=self.accent_color,
            fg=self.text_color,
            activebackground="#00A69A",
            activeforeground=self.text_color,
            bd=0,
            relief=tk.FLAT,
            padx=30,
            pady=15,
            state=tk.DISABLED
        )
        self.process_btn.pack(side=tk.LEFT, padx=15)
        self.process_btn.bind("<Enter>", lambda e: self.process_btn.config(bg="#00A69A"))
        self.process_btn.bind("<Leave>", lambda e: self.process_btn.config(bg=self.accent_color))
        
        # File label - centered
        self.file_label = tk.Label(
            main_frame,
            text="No file selected",
            font=("Segoe UI", base_font_size - 1, "italic"),
            fg="#B0BEC5",
            bg=self.bg_color
        )
        self.file_label.pack(pady=15)
        
        # Status frame - centered
        status_frame = tk.Frame(
            main_frame,
            bg=self.frame_color,
            bd=2,
            relief=tk.RAISED,
            padx=20,
            pady=15
        )
        status_frame.pack(pady=20)
        
        # Inspection result label - centered
        self.inspection_label = tk.Label(
            status_frame,
            text="Inspection Status: Not processed",
            font=("Segoe UI", base_font_size + 1, "bold"),
            fg=self.secondary_color,
            bg=self.frame_color
        )
        self.inspection_label.pack(pady=8)
        
        # Defect analysis label - centered
        self.analysis_label = tk.Label(
            status_frame,
            text="Defect Analysis: Waiting for processing",
            font=self.label_font,
            fg=self.text_color,
            bg=self.frame_color
        )
        self.analysis_label.pack(pady=8)
        
        # Image frame - centered
        self.images_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.images_frame.pack(pady=20)
        
        # Processed image frame - centered
        self.processed_frame = tk.Frame(
            self.images_frame,
            bg=self.frame_color,
            bd=3,
            relief=tk.SOLID
        )
        self.processed_frame.pack()
        
        # Processed image label - centered
        self.processed_label = tk.Label(
            self.processed_frame,
            text="Processed image with detections will appear here",
            font=self.label_font,
            fg="#B0BEC5",
            bg=self.frame_color,
            padx=50,
            pady=50
        )
        self.processed_label.pack()
        
        # Results text area frame - centered
        text_outer_frame = tk.Frame(main_frame, bg=self.bg_color)
        text_outer_frame.pack(pady=20)
        
        text_frame = tk.Frame(text_outer_frame, bg=self.bg_color)
        text_frame.pack()
        
        # Calculate text area size based on screen
        text_width = min(100, max(60, int(screen_width / 15)))
        text_height = min(15, max(10, int(screen_height / 60)))
        
        self.result_text = tk.Text(
            text_frame,
            height=text_height,
            width=text_width,
            font=self.text_font,
            bg=self.frame_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        scrollbar = tk.Scrollbar(
            text_frame,
            orient=tk.VERTICAL,
            command=self.result_text.yview,
            bg=self.bg_color,
            troughcolor=self.frame_color,
            highlightthickness=0
        )
        self.result_text.config(yscrollcommand=scrollbar.set)
        self.result_text.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.selected_image_path = None
        
        # Bind mousewheel to canvas
        main_canvas.bind_all("<MouseWheel>", lambda e: main_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select PCB Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("All files", "*.*")]
        )
        if file_path:
            self.selected_image_path = file_path
            self.file_label.config(text=f"Selected: {file_path.split('/')[-1]}")
            self.process_btn.config(state=tk.NORMAL)
    
    def process_image(self):
        if not self.selected_image_path:
            messagebox.showerror("Error", "Please select an image first")
            return
        
        self.process_btn.config(text="Processing...", state=tk.DISABLED)
        self.root.update()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Processing image...\n")
        
        result = process_image(self.selected_image_path)
        
        # Update status labels
        self.inspection_label.config(text=f"Inspection Status: {result['inspection_result']}")
        if result['predictions']:
            self.analysis_label.config(text=f"Total: {len(result['predictions'])} defects | Primary Type: {result['majority_class']}")
        else:
            self.analysis_label.config(text="No defects detected")
        
        # Display results
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "=== INSPECTION RESULT ===\n")
        self.result_text.insert(tk.END, f"Status: {result['inspection_result']}\n\n")
        
        self.result_text.insert(tk.END, "=== DEFECT ANALYSIS ===\n")
        if result['predictions']:
            self.result_text.insert(tk.END, f"Total Detections: {len(result['predictions'])}\n")
            self.result_text.insert(tk.END, f"Primary Defect Type: {result['majority_class']}\n\n")
            self.result_text.insert(tk.END, "Class Distribution:\n")
            for class_name, count in result['class_counts'].items():
                percentage = (count / len(result['predictions'])) * 100
                self.result_text.insert(tk.END, f"  • {class_name}: {count} ({percentage:.1f}%)\n")
            self.result_text.insert(tk.END, "\n")
        else:
            self.result_text.insert(tk.END, "No defects detected\n\n")
        
        # Display visualization image
        if result['vis_img']:
            # Responsive image sizing based on screen
            screen_width = self.root.winfo_screenwidth()
            max_width = min(1200, int(screen_width * 0.6))
            max_height = min(800, int(screen_width * 0.4))
            
            vis_display = result['vis_img'].copy()
            vis_display.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            vis_photo = ImageTk.PhotoImage(vis_display)
            self.processed_label.config(image=vis_photo, text="")
            self.processed_label.image = vis_photo
            self.result_text.insert(tk.END, "✓ Visualization image loaded\n")
            self.result_text.insert(tk.END, "✓ Saved as 'visualization_output.png'\n")
        else:
            self.processed_label.config(image="", text="No visualization image available")
            self.result_text.insert(tk.END, "✗ No visualization image available\n")
        
        # Display detailed predictions
        self.result_text.insert(tk.END, "\n=== DETAILED DETECTIONS ===\n")
        if result['predictions']:
            for i, pred in enumerate(result['predictions'], 1):
                self.result_text.insert(tk.END, f"Detection {i}:\n")
                self.result_text.insert(tk.END, f"  Type: {pred.get('class', 'Unknown')}\n")
                self.result_text.insert(tk.END, f"  Confidence: {pred.get('confidence', 0):.1%}\n")
                self.result_text.insert(tk.END, f"  Position: ({pred.get('x', 0):.0f}, {pred.get('y', 0):.0f})\n")
                self.result_text.insert(tk.END, f"  Size: {pred.get('width', 0):.0f} × {pred.get('height', 0):.0f} px\n")
                self.result_text.insert(tk.END, "-" * 40 + "\n")
        else:
            self.result_text.insert(tk.END, "No detections found\n")
        
        self.result_text.see(tk.END)
        self.process_btn.config(text="Process Image", state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = PCBInspectionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()