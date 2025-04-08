import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
from pathlib import Path

class MovToMp4Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("MOV → MP4 Dönüştürücü")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Ana çerçeve oluşturma
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Stiller ve temalar tanımlama
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10))
        style.configure("TLabel", font=("Arial", 10))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        
        # Dosya seçim alanı
        file_frame = ttk.LabelFrame(main_frame, text="Dosya/Klasör Seçimi", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(file_frame, text="Dosya Seç", command=self.select_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Klasör Seç", command=self.select_folder).pack(side=tk.LEFT, padx=5)
        
        # Çıktı klasörü seçim alanı
        output_frame = ttk.LabelFrame(main_frame, text="Çıktı Klasörü (Opsiyonel)", padding="10")
        output_frame.pack(fill=tk.X, pady=10)
        
        self.output_path_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Klasör Seç", command=self.select_output_folder).pack(side=tk.LEFT, padx=5)
        
        # Ayarlar alanı
        settings_frame = ttk.LabelFrame(main_frame, text="Dönüştürme Ayarları", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Codec seçimi
        codec_frame = ttk.Frame(settings_frame)
        codec_frame.pack(fill=tk.X, pady=5)
        ttk.Label(codec_frame, text="Video Codec:").pack(side=tk.LEFT, padx=5)
        
        self.codec_var = tk.StringVar(value="h264")
        ttk.Radiobutton(codec_frame, text="H.264", variable=self.codec_var, value="h264").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(codec_frame, text="HEVC (H.265)", variable=self.codec_var, value="hevc").pack(side=tk.LEFT, padx=10)
        
        # Kalite seçimi
        quality_frame = ttk.Frame(settings_frame)
        quality_frame.pack(fill=tk.X, pady=5)
        ttk.Label(quality_frame, text="Video Kalitesi:").pack(side=tk.LEFT, padx=5)
        
        self.quality_var = tk.StringVar(value="medium")
        ttk.Radiobutton(quality_frame, text="Düşük", variable=self.quality_var, value="low").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(quality_frame, text="Orta", variable=self.quality_var, value="medium").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(quality_frame, text="Yüksek", variable=self.quality_var, value="high").pack(side=tk.LEFT, padx=10)
        
        # İlerleme çubuğu
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_label = ttk.Label(progress_frame, text="Hazır")
        self.progress_label.pack(fill=tk.X, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)
        
        # İşlem durumu listesi
        status_frame = ttk.LabelFrame(main_frame, text="İşlem Durumu", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.status_text = tk.Text(status_frame, height=10, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.status_text.config(yscrollcommand=scrollbar.set)
        
        # Dönüştür butonu
        self.convert_button = ttk.Button(main_frame, text="Dönüştür", command=self.start_conversion, style="TButton")
        self.convert_button.pack(pady=10)
        
        # Durum değişkenleri
        self.is_converting = False
        self.total_files = 0
        self.processed_files = 0
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="MOV Dosyası Seç",
            filetypes=[("MOV Dosyaları", "*.mov"), ("Tüm Dosyalar", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="MOV Dosyalarını İçeren Klasör Seç")
        if folder_path:
            self.file_path_var.set(folder_path)
            
    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title="Çıktı Klasörü Seç")
        if folder_path:
            self.output_path_var.set(folder_path)
            
    def log_message(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        
    def update_progress(self, current, total):
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.progress_label.config(text=f"İşleniyor: {current}/{total} ({progress:.1f}%)")
        
    def start_conversion(self):
        if self.is_converting:
            messagebox.showwarning("Uyarı", "Dönüştürme işlemi devam ediyor!")
            return
            
        input_path = self.file_path_var.get()
        output_path = self.output_path_var.get() or None
        codec = self.codec_var.get()
        quality = self.quality_var.get()
        
        if not input_path:
            messagebox.showerror("Hata", "Lütfen bir dosya veya klasör seçin!")
            return
            
        # Dönüştürme işlemini ayrı bir thread'de başlat
        self.is_converting = True
        self.convert_button.config(state=tk.DISABLED)
        self.log_message("Dönüştürme işlemi başlıyor...")
        
        conversion_thread = threading.Thread(
            target=self.convert_files,
            args=(input_path, output_path, codec, quality)
        )
        conversion_thread.daemon = True
        conversion_thread.start()
        
    def conversion_completed(self, success):
        self.is_converting = False
        self.convert_button.config(state=tk.NORMAL)
        
        if success:
            self.log_message("Tüm dönüştürme işlemleri başarıyla tamamlandı!")
            messagebox.showinfo("Başarılı", "Dönüştürme işlemi tamamlandı!")
        else:
            self.log_message("Dönüştürme sırasında hatalar oluştu. Lütfen detayları kontrol edin.")
            messagebox.showwarning("Uyarı", "Bazı dosyaları dönüştürürken sorun yaşandı.")
            
    def convert_files(self, input_path, output_path, codec, quality):
        """Dosyaları dönüştüren ana işlev"""
        try:
            input_path = Path(input_path)
            
            # FFmpeg'in yüklü olup olmadığını kontrol et
            try:
                subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                self.root.after(0, lambda: self.log_message("Hata: FFmpeg bulunamadı! Lütfen FFmpeg'i yükleyin."))
                self.root.after(0, lambda: self.conversion_completed(False))
                return
                
            # Kalite ayarları
            quality_presets = {
                "low": "23",     # Düşük kalite, daha küçük dosya
                "medium": "20",  # Orta kalite
                "high": "17"     # Yüksek kalite, daha büyük dosya
            }
            crf = quality_presets.get(quality, "20")
            
            # Dosya listesini hazırla
            if input_path.is_file():
                if input_path.suffix.lower() != '.mov':
                    self.root.after(0, lambda: self.log_message(f"Hata: {input_path} bir MOV dosyası değil."))
                    self.root.after(0, lambda: self.conversion_completed(False))
                    return
                files_to_convert = [input_path]
            elif input_path.is_dir():
                files_to_convert = list(input_path.glob("*.mov")) + list(input_path.glob("*.MOV"))
                if not files_to_convert:
                    self.root.after(0, lambda: self.log_message(f"Uyarı: {input_path} klasöründe MOV dosyası bulunamadı."))
                    self.root.after(0, lambda: self.conversion_completed(False))
                    return
            else:
                self.root.after(0, lambda: self.log_message(f"Hata: {input_path} bulunamıyor."))
                self.root.after(0, lambda: self.conversion_completed(False))
                return
                
            # Çıktı klasörünü hazırla
            if output_path:
                output_path = Path(output_path)
                if not output_path.exists():
                    output_path.mkdir(parents=True)
            else:
                if input_path.is_file():
                    output_path = input_path.parent
                else:
                    output_path = input_path
                    
            # Toplam dosya sayısını ayarla
            self.total_files = len(files_to_convert)
            self.processed_files = 0
            
            success = True
            
            # Her dosyayı dönüştür
            for mov_file in files_to_convert:
                if input_path.is_file():
                    # Tek dosya için çıktı yolu
                    if output_path.is_dir():
                        out_file = output_path / f"{mov_file.stem}.mp4"
                    else:
                        out_file = output_path
                else:
                    # Klasör için çıktı yolu
                    out_file = output_path / f"{mov_file.stem}.mp4"
                    
                # Dönüştürme durumunu güncelle
                self.root.after(0, lambda msg=f"Dönüştürülüyor: {mov_file.name} -> {out_file.name}": self.log_message(msg))
                
                # FFmpeg komutunu oluştur ve çalıştır
                cmd = [
                    "ffmpeg",
                    "-i", str(mov_file),
                    "-c:v", codec,
                    "-crf", crf,
                    "-preset", "medium",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-y",
                    str(out_file)
                ]
                
                process = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                
                # Sonucu kontrol et
                self.processed_files += 1
                
                if process.returncode != 0:
                    error_msg = process.stderr.decode()
                    self.root.after(0, lambda msg=f"Hata: {mov_file.name} dönüştürülemedi": self.log_message(msg))
                    self.root.after(0, lambda msg=error_msg: self.log_message(msg))
                    success = False
                else:
                    self.root.after(0, lambda msg=f"Başarılı: {out_file.name} oluşturuldu.": self.log_message(msg))
                
                # İlerleme çubuğunu güncelle
                self.root.after(0, lambda c=self.processed_files, t=self.total_files: self.update_progress(c, t))
            
            # İşlem tamamlandı
            self.root.after(0, lambda s=success: self.conversion_completed(s))
            
        except Exception as e:
            self.root.after(0, lambda msg=f"Beklenmeyen hata: {str(e)}": self.log_message(msg))
            self.root.after(0, lambda: self.conversion_completed(False))

# Ana uygulama başlatma
if __name__ == "__main__":
    root = tk.Tk()
    app = MovToMp4Converter(root)
    root.mainloop()