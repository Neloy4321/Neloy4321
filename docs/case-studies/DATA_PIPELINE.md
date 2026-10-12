# Data Engineering Case Study
### Geo-Business Discovery & Collection Pipeline

**Domain:** Data acquisition, extraction and transformation  
**Core tools:** Node.js · JavaScript · Playwright · CSV  
**Source:** [Enterprise Geo-Business Discovery repository](https://github.com/Neloy4321/Enterprise-Geo-Business-Discovery-Data-Collection-Pipeline)

---

## The problem

Public business search results often provide useful location-based details, but collecting and structuring them manually is difficult to repeat across large datasets. This project approaches the work as a **multi-stage pipeline**, separating URL discovery, URL normalization, detail extraction and structured export.

## Architecture

```text
Google Maps search
         |
   Manual URL discovery
         |
    TXT collections
         |
 convert_all_to_json.js
         |
  urls.json + deduplication
         |
     final_scraper.js
         |
Business detail extraction
         |
      output.csv
```

This distinction is intentional: **the initial URL collection is manually initiated**, while the transformation and detail-extraction stages use the provided scripts. The repository does not demonstrate an unattended search-discovery service.

## Engineering decisions

| Decision | Technical reason |
| :--- | :--- |
| Separate URL preparation from extraction | Each stage can be checked and rerun independently |
| Remove duplicate URLs before extraction | Reduce redundant visits and duplicate records |
| Use Playwright for detail retrieval | Handle structured information from browser-rendered pages |
| Batch collected input | Organize different business categories or regions |
| Export a consistent CSV schema | Make downstream review and analysis easier |

The project extracts fields such as **business name, category, address, phone, region, plus code and website**.

## Reported project evaluation

According to the project documentation, the workflow was tested against **10,000+ business records** across regions in the United States and United Kingdom. Manual checks reported approximate extraction accuracy of **98% for addresses** and **95%+ for phone and region**. These are **project-reported manual-check results**, not an independent audit or guarantee for other websites or regions.

## Engineering lessons

A reusable extraction pipeline needs more than a scraper: input quality, deduplication, retries and field-level validation determine whether the final dataset is useful.

## Evidence & implementation

- [Pipeline README and run instructions](https://github.com/Neloy4321/Enterprise-Geo-Business-Discovery-Data-Collection-Pipeline)
- [URL normalization script](https://github.com/Neloy4321/Enterprise-Geo-Business-Discovery-Data-Collection-Pipeline/blob/main/convert_all_to_json.js)
- [Business extraction script](https://github.com/Neloy4321/Enterprise-Geo-Business-Discovery-Data-Collection-Pipeline/blob/main/final_scraper.js)

**Scope:** Educational and analytical project. Anyone reproducing the workflow is responsible for website terms, applicable law, privacy and responsible data collection.

---

[← Profile](../../README.md) · [All public projects](../PROJECT_ATLAS.md) · [ML case study](./ML_SYSTEM.md)
