# Overview

GPT-Memory is a document catalog and indexing system designed to organize and summarize documents from multiple projects and chat conversations. The system processes various file types (PDFs, Word documents, images, text files, etc.) from uploaded archives and generates structured manifests with metadata including categories, tags, summaries, and file hashes. It operates in offline mode without requiring external APIs, making it suitable for local document management and organization.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Processing Pipeline
The system follows a multi-stage processing approach:
1. **File Ingestion** - Scans and indexes files from the `archives/` directory
2. **Metadata Extraction** - Generates SHA256 hashes, categorizes files, and creates normalized titles
3. **Manifest Generation** - Outputs structured data in both JSON and CSV formats
4. **Manual Updates** - Allows post-processing updates to summaries, categories, and tags

## File Organization Strategy
- **Input Directory**: `archives/` - Users upload ZIP files, folders, and individual documents
- **Output Directory**: `out/` - Contains generated MANIFEST.json and MANIFEST.csv files
- **Supported Formats**: Text files, PDFs, Word documents, Excel files, PowerPoint presentations, images (PNG, JPG, WebP), and ZIP archives

## Categorization System
Implements rule-based automatic categorization using path and filename analysis:
- **veganmapai** - VeganMap AI project files
- **health** - Health-related documents
- **marketing** - Business and marketing materials
- **screens** - Screenshots and visual assets
- **logs** - System logs and OAuth files
- **general** - Default category for uncategorized files

## Data Structure Design
Each document record contains:
- Unique ID (first 12 characters of SHA256 hash)
- Normalized title (cleaned filename without extension)
- Automatic or manual category assignment
- Flexible tagging system
- File metadata (size, date, URI, SHA256 hash)
- Optional summary field for manual annotation

## Error Handling and Validation
- Robust file path validation and normalization
- Duplicate detection using SHA256 hashing
- Graceful handling of corrupted or inaccessible files
- Progress tracking with visual indicators
- Data integrity validation for dates and tags

# External Dependencies

## Core Libraries
- **pandas** - Data manipulation and CSV generation
- **tqdm** - Progress bar visualization during file processing
- **pathlib** - Modern file path handling
- **hashlib** - SHA256 hash generation for file identification

## Platform-Specific Dependencies
- **python-magic-bin** (Windows) / **python-magic** (Unix) - File type detection and validation

## Optional Future Integrations
- **xxhash** - Alternative hashing algorithm for performance optimization
- Placeholder support for embeddings APIs and RAG (Retrieval-Augmented Generation) systems

## File System Requirements
- Local file system access for reading archives
- Write permissions for output directory creation
- Support for various file encodings (UTF-8 default)