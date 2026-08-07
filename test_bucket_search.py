import asyncio
import tempfile

from bucket_manager import BucketManager


def test_search_prefers_token_overlap_and_is_bounded():
    with tempfile.TemporaryDirectory() as directory:
        manager = BucketManager({
            "buckets_dir": directory,
            "matching": {"fuzzy_threshold": 0, "max_results": 5},
            "wikilink": {"enabled": False},
        })

        async def scenario():
            exact_id = await manager.create(
                "讨论 Python asyncio 的断线恢复和重试策略",
                name="SSE 断线恢复",
                tags=["Python", "asyncio"],
                domain=["工程"],
            )
            await manager.create(
                "记录周末去了咖啡店和朋友聊天",
                name="周末日记",
                tags=["生活"],
                domain=["生活"],
            )
            results = await manager.search("asyncio 断线恢复", limit=100)
            assert results[0]["id"] == exact_id
            assert len(results) <= 50

        asyncio.run(scenario())
