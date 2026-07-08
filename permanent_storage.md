# 💾 Permanent Storage & Document Management

## Overview

Your AI Knowledge Assistant now has **persistent storage** enabled. All uploaded documents, URLs, and indexed content are automatically saved to disk and survive application restarts.

## Storage Architecture

### Where Documents are Stored
```
chroma_store/
├── knowledge_base.json      # Main document storage (permanent)
└── metadata.json            # Document metadata & timestamps
```

### How It Works

1. **Upload a document** → Immediately indexed and saved to disk
2. **Add a website URL** → Content fetched, processed, and permanently stored
3. **Restart the app** → All documents are automatically loaded from storage
4. **Delete a document** → Permanently removed from disk

## Features

### ✅ Automatic Persistence
- All uploads automatically saved to `chroma_store/knowledge_base.json`
- Metadata tracking: timestamp, category, text length, chunk count
- No manual backup needed - data persists across sessions

### ✅ Document Management
- **View all documents** with chunk counts and categories
- **Delete documents** permanently with confirmation dialog
- **Track storage** stats (total chunks, text size, document count)
- **Monitor** persistence status in the UI

### ✅ Storage Indicators
- Green indicator in sidebar: "💾 Persistent Storage Active"
- Shows "Documents saved permanently" status
- Hover over documents to delete with ✕ button

## API Endpoints (New)

### Delete a Document Permanently
```bash
DELETE /api/document/{source}
```
**Example:**
```bash
curl -X DELETE http://localhost:8000/api/document/my_file.pdf
```

### Get Storage Statistics
```bash
GET /api/storage-stats
```
**Response:**
```json
{
  "status": "persistent_storage_active",
  "total_documents": 3,
  "total_chunks": 45,
  "total_text_size_chars": 25000,
  "storage_location": "./chroma_store/knowledge_base.json",
  "persistence": {
    "knowledge_base_file": "./chroma_store/knowledge_base.json",
    "auto_save": "enabled",
    "backup_enabled": "recommended"
  }
}
```

## Usage Examples

### Upload a Document (Persisted)
1. Click "➕ Add knowledge source"
2. Upload a file (txt, pdf, docx)
3. Select category
4. Document is immediately saved permanently

### Delete a Document
1. Hover over any document in the sidebar
2. Click the **✕** button
3. Confirm deletion
4. Document is permanently removed from storage

### Access Storage Stats
```javascript
// Frontend API
import { getStorageStats } from './api.js';

const stats = await getStorageStats();
console.log(`Total documents: ${stats.total_documents}`);
console.log(`Total chunks: ${stats.total_chunks}`);
```

## Data Structure

### knowledge_base.json Format
```json
[
  {
    "id": "document-name-abc12345-0",
    "source": "document-name.pdf",
    "category": "Academics",
    "text": "First chunk of text..."
  },
  {
    "id": "document-name-def67890-1",
    "source": "document-name.pdf",
    "category": "Academics",
    "text": "Second chunk of text..."
  }
]
```

### metadata.json Format
```json
{
  "document-name.pdf": {
    "added_at": "2026-07-07T10:30:45.123456",
    "category": "Academics",
    "chunks_count": 5,
    "text_length": 4230
  }
}
```

## Backup & Recovery

### Manual Backup
To backup your knowledge base:
```bash
# Copy the storage folder
cp -r chroma_store chroma_store.backup
```

### Restore from Backup
```bash
# Restore the storage folder
cp -r chroma_store.backup chroma_store
```

### Export Documents
All documents are stored in plain JSON format, so you can:
- Open `chroma_store/knowledge_base.json` in any text editor
- Copy/backup the entire `chroma_store/` folder
- Share the JSON file with others

## Storage Limits

| Metric | Recommendation |
|--------|-----------------|
| Total Documents | Unlimited |
| Total Chunks | Thousands (performance depends on search) |
| File Size per Upload | 50MB+ (depends on system) |
| Storage Disk Space | 100MB+ recommended for thousands of chunks |

## Troubleshooting

### "Storage not persistent"
- ✅ **Solution**: Restart the app - documents load automatically from `chroma_store/`
- Check that `chroma_store/knowledge_base.json` exists
- Look for file permission issues

### "Document deleted but still appears"
- ✅ **Solution**: Refresh the page (F5)
- Clear browser cache if needed
- Restart the app

### "Out of storage space"
- ✅ **Solution**: Delete old documents or back them up first
- Monitor file size: `chroma_store/knowledge_base.json`
- Move to external storage if needed

### "Can't delete a document"
- ✅ **Solution**: Check that the document name is correct
- Try refreshing and trying again
- Check browser console for error messages

## Security Considerations

⚠️ **Important Notes:**
- `chroma_store/` folder contains all your indexed documents
- **No encryption** by default - store sensitive data carefully
- **No access control** - anyone with file access can read documents
- For sensitive data, consider implementing encryption

## What's Saved Permanently?

| Item | Persisted | Details |
|------|-----------|---------|
| Uploaded documents | ✅ Yes | Stored in knowledge_base.json |
| Document metadata | ✅ Yes | Timestamps, categories, sizes |
| Chat history | ❌ No | Not saved (by design) |
| Suggested actions | ❌ No | Generated dynamically |
| API responses | ❌ No | Cached temporarily only |

## API Response Examples

### Upload Response (Saved Permanently)
```json
{
  "source": "university_handbook.pdf",
  "category": "Academics",
  "chunks_added": 12,
  "persisted": true
}
```

### Delete Response
```json
{
  "message": "Document 'university_handbook.pdf' permanently deleted.",
  "success": true
}
```

## Next Steps

1. ✅ Upload your documents - they're automatically saved
2. ✅ Restart the app - documents load automatically
3. ✅ Delete old documents when needed
4. ✅ Back up `chroma_store/` folder regularly

---

**All documents are saved permanently to disk!** 🎉
