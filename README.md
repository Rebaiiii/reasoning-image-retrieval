### Reasoning-Based Image Retrieval

Reasoning-Based Image Retrieval is a project for finding images from text descriptions that include spatial relationships or scene details. For example, a query such as "a red car behind a blue car" needs more than recognising the two cars.

The goal is to compare CLIP similarity search with a multimodal model that checks how well each retrieved image matches the query. The models are used without fine-tuning.

## Planned Approach

1. CLIP Retrieval: Convert images and text queries into embeddings, then rank the images by similarity.
2. Reasoning-Based Reranking: Use Qwen to check the objects and relationships in the retrieved images and reorder the results.
3. Evaluation: Compare the original CLIP rankings with the reranked results in terms of retrieval accuracy and computation time.

## Current Work

CLIP ViT-B/32 baseline and evaluation on a small set of labelled queries.
