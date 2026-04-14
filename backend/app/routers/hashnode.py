import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings

router = APIRouter()

HASHNODE_API = "https://gql.hashnode.com"


class HashnodePublishRequest(BaseModel):
    title: str
    markdown: str
    tags: list[str] = []


@router.post("/publish-hashnode")
async def publish_to_hashnode(req: HashnodePublishRequest):
    if not settings.hashnode_api_key or not settings.hashnode_publication_id:
        raise HTTPException(
            status_code=400,
            detail="Hashnode API key and Publication ID not configured. Add them to your .env file."
        )

    # Build tags as objects with name and slug
    tag_objects = []
    for tag in req.tags:
        tag_objects.append({
            "name": tag,
            "slug": tag.lower().replace(" ", "-"),
        })

    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
        publishPost(input: $input) {
            post {
                id
                title
                slug
                url
            }
        }
    }
    """

    variables = {
        "input": {
            "publicationId": settings.hashnode_publication_id,
            "title": req.title,
            "contentMarkdown": req.markdown,
        }
    }

    # Only add tags if provided
    if tag_objects:
        variables["input"]["tags"] = tag_objects

    try:
        response = requests.post(
            HASHNODE_API,
            json={"query": mutation, "variables": variables},
            headers={
                "Content-Type": "application/json",
                "Authorization": settings.hashnode_api_key,
            },
        )

        result = response.json()

        if "errors" in result:
            raise HTTPException(
                status_code=400,
                detail=f"Hashnode API error: {result['errors']}"
            )

        post = result["data"]["publishPost"]["post"]
        return {
            "success": True,
            "url": post["url"],
            "title": post["title"],
            "slug": post["slug"],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish: {str(e)}")