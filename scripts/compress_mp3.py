# scripts/compress_mp3.py - TAM İŞLƏYƏN VERSİYA
import os
import subprocess

def compress_mp3_files():
    input_folder = "Quran_mp3"
    output_folder = "Quran_mp3_compressed"
    
    # ✅ FFmpeg-in dəqiq yolu (sizin sisteminizə uyğun)
    ffmpeg_path = r"C:\Users\Farid.Huseynzada\Documents\ffmpeg\bin\ffmpeg.exe"
    
    # FFmpeg-in mövcudluğunu yoxla
    if not os.path.exists(ffmpeg_path):
        print(f"❌ FFmpeg tapılmadı: {ffmpeg_path}")
        print("📌 Zəhmət olmasa yolu yoxlayın")
        return
    
    print(f"✅ FFmpeg tapıldı: {ffmpeg_path}")
    print(f"📁 Versiya: {ffmpeg_version(ffmpeg_path)}")
    
    os.makedirs(output_folder, exist_ok=True)
    
    mp3_files = [f for f in os.listdir(input_folder) if f.endswith(".mp3")]
    
    if not mp3_files:
        print("❌ MP3 faylları tapılmadı!")
        return
    
    print(f"\n📊 {len(mp3_files)} MP3 faylı tapıldı\n")
    
    for i, filename in enumerate(mp3_files, 1):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        original_size = os.path.getsize(input_path) / (1024 * 1024)
        
        print(f"[{i}/{len(mp3_files)}] Sıxışdırılır: {filename} ({original_size:.1f} MB)")
        
        # FFmpeg ilə sıxışdır (64kbps, mono)
        cmd = [
            ffmpeg_path,
            "-i", input_path,
            "-b:a", "64k",
            "-ac", "1",
            "-y",  # Mövcud faylı üzərinə yaz
            output_path
        ]
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                timeout=300  # 5 dəqiqə vaxt limiti
            )
            
            if result.returncode == 0:
                compressed_size = os.path.getsize(output_path) / (1024 * 1024)
                saved = original_size - compressed_size
                
                if saved > 0:
                    print(f"   ✅ {compressed_size:.1f} MB (qənaət: {saved:.1f} MB, {saved/original_size*100:.0f}%)\n")
                else:
                    print(f"   ⚠️ {compressed_size:.1f} MB (kiçilmədi!)\n")
            else:
                print(f"   ❌ Xəta: {result.stderr[:200]}\n")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏱️ Zaman aşımı! (5 dəqiqədən çox çəkdi)\n")
        except Exception as e:
            print(f"   ❌ Xəta: {e}\n")
    
    print("=" * 50)
    print("✅ Sıxışdırma tamamlandı!")
    print(f"📁 Sıxışdırılmış fayllar: {output_folder}/")
    print("=" * 50)
    
    # Sıxışdırılmış faylları orijinal qovluğa köçür
    replace = input("\n🔁 Sıxışdırılmış faylları orijinallarla əvəz etmək istəyirsiniz? (y/n): ")
    if replace.lower() == 'y':
        for filename in mp3_files:
            src = os.path.join(output_folder, filename)
            dst = os.path.join(input_folder, filename)
            if os.path.exists(src):
                os.replace(src, dst)
                print(f"   ✅ {filename} əvəz olundu")
        print("\n✅ Bütün fayllar əvəz olundu!")
        print("🎯 İndi botu işə salıb sınaqdan keçirə bilərsiniz!")

def ffmpeg_version(ffmpeg_path):
    """FFmpeg versiyasını qaytarır"""
    try:
        result = subprocess.run([ffmpeg_path, '-version'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if 'ffmpeg version' in line:
                return line.split('ffmpeg version')[1].strip().split()[0]
    except:
        return 'məlum deyil'
    return 'məlum deyil'

if __name__ == "__main__":
    compress_mp3_files()