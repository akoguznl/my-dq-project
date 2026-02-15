import pandas as pd
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
import sys

# 1. Şemayı senin CSV'ndeki tam sütun isimlerine göre güncelliyoruz
class AmazonOrder(BaseModel):
    order_id: str  # Görseldeki gibi küçük harf
    Status: str
    Category: str
    Qty: int = Field(ge=0)
    Amount: Optional[float] = Field(None, ge=0)
    B2B: bool

def validate_data():
    try:
        # DtypeWarning hatasını engellemek için low_memory=False ekledik
        df = pd.read_csv('data/amazon_orders.csv', low_memory=False)
        
        # Sütun isimlerindeki olası boşlukları temizleyelim (garanti olsun)
        df.columns = [c.strip() for c in df.columns]
        
        records = df.to_dict(orient='records')
        
        for record in records:
            # NaN (boş) değerleri None'a çeviriyoruz ki Pydantic hata vermesin
            clean_record = {k: (None if pd.isna(v) else v) for k, v in record.items()}
            AmazonOrder(**clean_record)
        
        print(f"✅ Başarılı: {len(records)} satır veri kalite kontrolünden geçti.")
        sys.exit(0)

    except ValidationError as e:
        print("❌ Veri Kalite Hatası Tespit Edildi!")
        # Hangi satırda ne hatası olduğunu daha net görelim
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Beklenmedik Hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    validate_data()