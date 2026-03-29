# Aplikasi Perpustakaan dengan Redis
# Nama  : Fazar Adi Putra
# NIM   : 2311082016
# Kelas : TRPL 3B


from dataclasses import dataclass
from typing import Dict

import redis

@dataclass
class Book:
    id_buku: str
    judul: str
    pengarang: str
    stok: int
    kategori: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "id_buku": self.id_buku,
            "judul": self.judul,
            "pengarang": self.pengarang,
            "stok": str(self.stok),
            "kategori": self.kategori,
        }

    @classmethod
    def from_dict(cls, data: Dict[bytes, bytes]) -> "Book":
        decoded = {k.decode(): v.decode() for k, v in data.items()}
        return cls(
            id_buku=decoded.get("id_buku", ""),
            judul=decoded.get("judul", ""),
            pengarang=decoded.get("pengarang", ""),
            stok=int(decoded.get("stok", "0")),
            kategori=decoded.get("kategori", ""),
        )

REDIS_KEY_BASE = "library"

def main() -> None:
    r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=False)

    books = [
        Book(id_buku="BK001", judul="Belajar Python", pengarang="Agus Kurniawan", stok=5, kategori="Pemrograman"),
        Book(id_buku="BK002", judul="Algoritma dan Struktur Data", pengarang="Rinaldi Munir", stok=3, kategori="Ilmu Komputer"),
        Book(id_buku="BK003", judul="Basis Data", pengarang="Fathansyah", stok=7, kategori="Database"),
        Book(id_buku="BK004", judul="Jaringan Komputer", pengarang="Andrew Tanenbaum", stok=4, kategori="Jaringan"),
        Book(id_buku="BK005", judul="Kecerdasan Buatan", pengarang="Stuart Russell", stok=2, kategori="AI"),
    ]

    for book in books:
        key = f"{REDIS_KEY_BASE}:{book.id_buku}"
        r.hset(key, mapping=book.to_dict())

    print("=== DATA PERPUSTAKAAN (DARI REDIS) ===")
    for book in books:
        key = f"{REDIS_KEY_BASE}:{book.id_buku}"
        stored = r.hgetall(key)
        if stored:
            b = Book.from_dict(stored)
            print(f"[{b.id_buku}] {b.judul} | Pengarang: {b.pengarang} | Stok: {b.stok} | Kategori: {b.kategori}")

if __name__ == "__main__":
    main()
