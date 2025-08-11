# Dokumentasi API - SuperBoost AllerScan

## Base URL
- **Development**: http://localhost:8001
- **Production**: https://your-domain.com

## Interactive Documentation
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## Authentication

### Login Admin
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "your-password"
}
```

**Response:**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "username": "admin",
    "role": "admin"
  }
}
```

## Prediction Endpoints

### Prediksi Alergen
**Endpoint utama untuk deteksi alergen makanan**

```http
POST /api/v1/predict
Content-Type: application/json

{
  "nama_produk_makanan": "Roti Gandum",
  "bahan_utama": "Tepung gandum, ragi, gula",
  "pemanis": "Gula pasir", 
  "lemak_minyak": "Mentega",
  "penyedap_rasa": "Vanila",
  "alergen": "Gluten"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "product_name": "Roti Gandum",
    "prediction": "Mengandung Alergen",
    "confidence_score": 0.947,
    "risk_level": "high",
    "allergen_count": 2,
    "detected_allergens": [
      {
        "allergen": "gluten",
        "confidence": 0.95,
        "category": "grains"
      },
      {
        "allergen": "susu",
        "confidence": 0.78,
        "category": "dairy"
      }
    ],
    "processing_time_ms": 245.67,
    "model_version": "1.0",
    "created_at": "2025-08-11T10:30:00Z"
  }
}
```

### Supported Allergens
```http
GET /api/v1/predict/supported-allergens
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_allergens": 23,
    "categories": {
      "grains": ["gandum", "gluten", "barley"],
      "dairy": ["susu", "laktosa", "casein", "whey"],
      "eggs": ["telur", "albumin"],
      "nuts": ["kacang tanah", "almond", "kenari", "mete"],
      "seafood": ["ikan", "udang", "kerang", "cumi"],
      "soy": ["kedelai", "kacang kedelai"],
      "additives": ["msg", "sulfites", "tartrazine"]
    }
  }
}
```

### Health Check
```http
GET /api/v1/predict/health
```

**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "database": "connected",
  "model": "loaded",
  "version": "1.0.0",
  "uptime": "2h 30m 15s"
}
```

## Dataset Endpoints

### Get Dataset dengan Pagination
```http
GET /api/v1/dataset?page=1&page_size=20&sort_by=created_at&sort_order=desc
```

**Query Parameters:**
- `page` (int): Nomor halaman (default: 1)
- `page_size` (int): Jumlah item per halaman (default: 20, max: 100)
- `sort_by` (string): Field untuk sorting (created_at, confidence_score, product_name)
- `sort_order` (string): Urutan sorting (asc, desc)
- `search` (string): Search berdasarkan nama produk
- `risk_level` (string): Filter berdasarkan tingkat risiko
- `date_from` (string): Filter tanggal mulai (YYYY-MM-DD)
- `date_to` (string): Filter tanggal akhir (YYYY-MM-DD)

**Response:**
```json
{
  "success": true,
  "data": {
    "records": [
      {
        "id": 1,
        "product_name": "Roti Gandum",
        "ingredients_input": "Tepung gandum, ragi, gula",
        "predicted_allergens": "Gluten, Susu",
        "allergen_count": 2,
        "confidence_score": 0.947,
        "risk_level": "high",
        "processing_time_ms": 245.67,
        "created_at": "2025-08-11T10:30:00Z",
        "bahan_utama": "Tepung gandum",
        "pemanis": "Gula pasir",
        "lemak_minyak": "Mentega",
        "penyedap_rasa": "Vanila"
      }
    ],
    "pagination": {
      "total_records": 500,
      "total_pages": 25,
      "current_page": 1,
      "page_size": 20,
      "has_next": true,
      "has_prev": false,
      "next_page": 2,
      "prev_page": null
    }
  }
}
```

### Dataset Statistics
```http
GET /api/v1/dataset/statistics
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_predictions": 500,
    "risk_distribution": {
      "none": 120,
      "low": 180,
      "medium": 150,
      "high": 50
    },
    "confidence_distribution": {
      "0.0-0.3": 25,
      "0.3-0.5": 45,
      "0.5-0.7": 180,
      "0.7-0.9": 200,
      "0.9-1.0": 50
    },
    "top_allergens": [
      {"allergen": "gluten", "count": 150},
      {"allergen": "susu", "count": 120},
      {"allergen": "telur", "count": 100}
    ],
    "daily_predictions": [
      {"date": "2025-08-10", "count": 25},
      {"date": "2025-08-11", "count": 30}
    ],
    "avg_confidence_score": 0.78,
    "avg_processing_time_ms": 234.5
  }
}
```

### Export ke Excel
```http
GET /api/v1/dataset/export/excel?limit=1000&format=standard
```

**Query Parameters:**
- `limit` (int): Maksimum records untuk export (default: 1000)
- `format` (string): Format export ('standard', 'detailed', 'summary')
- `include_stats` (boolean): Include statistics sheet (default: true)

**Response:** File Excel download

### Delete Prediction
```http
DELETE /api/v1/dataset/predictions/{prediction_id}
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "success": true,
  "message": "Prediksi berhasil dihapus",
  "deleted_id": 123
}
```

## Error Handling

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Input tidak valid",
    "details": {
      "field": "nama_produk_makanan",
      "reason": "Field wajib diisi"
    }
  },
  "timestamp": "2025-08-11T10:30:00Z"
}
```

### HTTP Status Codes

| Status Code | Description | 
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Input tidak valid |
| 401 | Unauthorized - Token tidak valid |
| 403 | Forbidden - Akses ditolak |
| 404 | Not Found - Endpoint/resource tidak ditemukan |
| 422 | Validation Error - Data tidak sesuai schema |
| 500 | Internal Server Error - Error server |
| 503 | Service Unavailable - Database/ML model tidak tersedia |

### Common Error Codes

| Error Code | Description |
|------------|-------------|
| `VALIDATION_ERROR` | Input validation gagal |
| `MODEL_ERROR` | Error pada ML model |
| `DATABASE_ERROR` | Error koneksi database |
| `AUTHENTICATION_ERROR` | Error autentikasi |
| `AUTHORIZATION_ERROR` | Error autorisasi |
| `RATE_LIMIT_ERROR` | Terlalu banyak request |

## Rate Limiting

- **Prediction API**: 100 requests per minute per IP
- **Dataset API**: 50 requests per minute per IP
- **Export API**: 5 requests per minute per user

## Model Information

### Model Metrics
```http
GET /api/v1/model/info
```

**Response:**
```json
{
  "success": true,
  "data": {
    "model_name": "SVM + AdaBoost Ensemble",
    "version": "1.0.0",
    "accuracy": 0.937,
    "precision": 0.912,
    "recall": 0.898,
    "f1_score": 0.905,
    "training_date": "2025-01-15",
    "training_samples": 2000,
    "supported_allergens": 23,
    "last_updated": "2025-08-11T10:30:00Z"
  }
}
```

## Request Examples (cURL)

### Prediksi Basic
```bash
curl -X POST "http://localhost:8001/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "nama_produk_makanan": "Biskuit Coklat",
       "bahan_utama": "Tepung terigu, coklat, susu",
       "pemanis": "Gula pasir",
       "lemak_minyak": "Minyak kelapa sawit",
       "penyedap_rasa": "Vanilla, lesitin kedelai"
     }'
```

### Get Dataset dengan Filter
```bash
curl "http://localhost:8001/api/v1/dataset?page=1&page_size=10&risk_level=high&search=roti"
```

### Export Excel
```bash
curl -o export.xlsx "http://localhost:8001/api/v1/dataset/export/excel?limit=500"
```

## Testing API

### Postman Collection
Import collection dari: `docs/postman/AllerScan-API.postman_collection.json`

### Insomnia Workspace
Import workspace dari: `docs/insomnia/allerscan-workspace.json`
