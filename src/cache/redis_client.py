import redis
import json


redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)


def save_product_state(
    product_id,
    state
):

    redis_client.set(
        f"product:{product_id}:state",
        json.dumps(state, default=str)
    )


def get_product_state(product_id):

    data = redis_client.get(
        f"product:{product_id}:state"
    )

    if data:

        return json.loads(data)

    return None
