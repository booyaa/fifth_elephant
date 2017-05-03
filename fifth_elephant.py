import os
import json
import pickle

from mastodon import Mastodon


def init():
    """
    Creates a mastodon session, using cached credentials

    Returns: mastodon instance
    """
    file_path = "/Users/booyaa/.config.fifth_elephant"
    with open(file_path, 'rb') as f:
        raw = f.read()

    secrets = json.loads(raw)
    if secrets is None:
        print("Failed to parse config file!")
        os.sys.exit(-1)

    our_client_id = os.environ['FE_CLIENT_ID']
    our_client_secret = os.environ['FE_CLIENT_SECRET']
    our_access_token = secrets["access_token"]
    return Mastodon(client_id=our_client_id,
                    client_secret=our_client_secret, access_token=our_access_token)


def save(toots):
    """
    Pickles toots
    Args: toots to be pickled
    """
    file_path = os.path.join(".", "dontcommitmebro", "toots.pickle")
    with open(file_path, "wb") as f:
        pickle.dump(toots, f)

    print("cached toots!")


def setup():
    mastodon = init()
    data = mastodon.timeline_local(limit=25)
    save(data)


def load():
    """
    Unpickles toots
    Returns: toots
    """
    file_path = os.path.join(".", "dontcommitmebro", "toots.pickle")
    with open(file_path, "rb") as f:
        return pickle.load(f)


if __name__ == '__main__':
    # setup()
    toots = load()
    print("no of toots: {}\n1st toot:\n{}".format(len(toots), toots[0]))
    for toot in toots:
        print("@{} {} ({})".format(toot['account']['username'],
                                   toot['content'],
                                   toot['created_at']))
