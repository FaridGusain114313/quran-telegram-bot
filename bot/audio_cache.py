# bot/audio_cache.py
import os
from io import BytesIO
from typing import Optional

# Global cache (RAM-da saxlanılır)
_surah_audio_cache = {}

def get_surah_audio(surah_no: int, mp3_folder: str = "Quran_mp3") -> Optional[BytesIO]:
    """
    Surə audio faylını cache-dən və ya diskdən qaytarır
    """
    # Əvvəlcə cache-də yoxla
    if surah_no in _surah_audio_cache:
        audio_data = _surah_audio_cache[surah_no]
        audio_data.seek(0)
        return audio_data
    
    # Cache-də yoxdursa, diskdən oxu
    mp3_path = os.path.join(mp3_folder, f"{surah_no:03d}.mp3")
    
    if not os.path.exists(mp3_path):
        mp3_path = os.path.join(mp3_folder, f"{surah_no}.mp3")
    
    if not os.path.exists(mp3_path):
        mp3_path = os.path.join(mp3_folder, f"surah_{surah_no}.mp3")
    
    if not os.path.exists(mp3_path):
        print(f"⚠️ Audio faylı tapılmadı: {mp3_path}")
        return None
    
    try:
        with open(mp3_path, 'rb') as f:
            audio_data = BytesIO(f.read())
            audio_data.name = f"{surah_no:03d}.mp3"
        
        _surah_audio_cache[surah_no] = audio_data
        print(f"✅ Cache-ə əlavə edildi: {surah_no}. surə ({len(audio_data.getbuffer()) / 1024:.1f} KB)")
        
        return audio_data
    except Exception as e:
        print(f"❌ Audio oxuma xətası ({surah_no}): {e}")
        return None

def clear_audio_cache():
    """Cache-i təmizlə"""
    global _surah_audio_cache
    _surah_audio_cache.clear()
    print("🗑️ Audio cache təmizləndi")

def get_cache_stats() -> dict:
    """Cache statistikasını qaytarır"""
    total_size = 0
    for audio_data in _surah_audio_cache.values():
        total_size += len(audio_data.getbuffer())
    
    return {
        "count": len(_surah_audio_cache),
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "surahs": list(_surah_audio_cache.keys())
    }

def is_cached(surah_no: int) -> bool:
    """Verilən surənin cache-də olub-olmadığını yoxlayır"""
    return surah_no in _surah_audio_cache