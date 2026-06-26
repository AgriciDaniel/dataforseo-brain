---
type: platform
title: "YouTube as a DataForSEO Surface"
domain: dataforseo
subdomain: serp
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, serp, youtube, video]
related:
  - "[[cap-serp-non-google-engines]]"
  - "[[cap-serp-api]]"
  - "[[play-content-strategy-brief]]"
---

# YouTube as a DataForSEO Surface

> YouTube search results, per-video metrics, comments, and transcripts exposed through the SERP API as a video search and discovery surface. Sits under [[index|DataForSEO Brain]] then [[platforms/_index|Platforms]].

## Overview
YouTube is treated by DataForSEO as a search engine in its own right under `serp/youtube`. The module covers four endpoints: organic search results, single-video metadata and metrics, video comments, and video subtitles/transcripts. This makes YouTube a tractable surface for video rank tracking, competitor channel analysis, sentiment mining on comments, and transcript extraction for content repurposing. YouTube also matters for AI visibility: research shows it has become one of the most-cited domains inside Google AI Overviews, so YouTube presence feeds generative search exposure.

## What it covers
- `serp/youtube/organic` returns up to 20 result blocks (1-200 via `block_depth`): `youtube_video`, `youtube_channel`, and `youtube_playlist` items.
- `serp/youtube/video_info` returns one video's full metadata and metrics (views, likes, comments count, subscriber count, streaming quality variants, subtitles list).
- `serp/youtube/video_comments` returns top comments (default 20, max 200) with author, text, likes, and reply counts.
- `serp/youtube/video_subtitles` returns transcript segments with timing, optionally translated into 150+ languages.

## Key parameters / inputs
- Organic: `keyword` (up to 700 chars), one location field, one language field, `block_depth` (1-200, default 20), `device`.
- Video Info / Comments / Subtitles: `video_id` (the YouTube identifier from a URL or organic result), one location field, one language field.
- Comments: `depth` (default 20, max 200).
- Subtitles: `subtitles_language` (original-text language) and `subtitles_translate_language` (target for translation, 150+ supported).

## Response / what you get back
- `youtube_video`: `video_id`, `title`, `url`, `channel_name`, `views_count`, `duration_time_seconds`, `publication_date`, `is_live`, `is_shorts`.
- `youtube_channel`: `channel_id`, `name`, `url`, `video_count`, `is_verified`, `description`.
- Video Info item: `views_count`, `likes_count`, `comments_count`, `channel_subscribers_count` (displayed_count and count), `keywords`, `category`, `streaming_quality[]` (label, width, height, bitrate, fps, mime_type), `subtitles[]`. Cost is about $0.006 per request.
- `youtube_comment`: `author_name`, `author_url`, `text`, `publication_date`, `likes_count`, `reply_count`.
- `youtube_subtitles`: `text`, `start_time`, `end_time`, `duration_time`.

## Cost & method notes
- All four endpoints offer Standard (POST then Task GET Advanced) and Live Advanced; Advanced is the only result format. See [[cap-task-vs-live-execution]].
- Charged per request; Video Info is roughly $0.006 per call. See [[cap-queue-priority-cost-model]].
- Video Info, Comments, and Subtitles run on `desktop` only and accept one task per call.

## When to use / how it fits
- Mining video SERPs and transcripts for a content brief: [[play-content-strategy-brief]].
- Tracking video rankings alongside web rank tracking: [[play-rank-tracking-pipeline]].
- Feeding YouTube presence into AI-visibility tracking, since YouTube is heavily cited in AI Overviews: [[play-ai-visibility-tracking]].
- Sentiment analysis on comment text complements [[cap-content-analysis-api]].

## Gotchas / limits
- Organic results are counted in blocks, not flat results; `block_depth` controls volume.
- `video_id` is mandatory for Info, Comments, and Subtitles, and those run desktop-only.
- 2000 calls/min; one task per Info/Subtitles call. See [[cap-rate-limits-throughput]].
- Subtitle translation depends on the original transcript being available; auto-captions vary by video.
- `views_count`, `likes_count`, and `channel_subscribers_count` are point-in-time captures at request time, not a time series, so trend tracking requires repeated calls and your own storage.
- `is_shorts` on organic items distinguishes Shorts from standard videos, which matters when analyzing a channel's format mix.

## Related
- [[cap-serp-non-google-engines]]
- [[cap-serp-api]]
- [[cap-content-analysis-api]]
- [[cap-task-vs-live-execution]]
- [[cap-locations-languages-targeting]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[cap-geo-ai-search-optimization]]
- [[play-content-strategy-brief]]
- [[play-ai-visibility-tracking]]
- [[plat-ai-assistants]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[platforms/_index]]

## Sources
- https://docs.dataforseo.com/v3/serp/youtube/organic/live/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/serp/youtube/video_info/live/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/serp/youtube/video_comments/live/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/serp/youtube/video_subtitles/live/advanced/ - retrieved 2026-06-26
