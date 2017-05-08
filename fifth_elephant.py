import os
import json
import pickle

from mastodon import Mastodon
from bs4 import BeautifulSoup


def init(instance):
    """
    Creates a mastodon session, using cached credentials

    Args: instance - to access
    Returns: mastodon instance
    """

    home = os.environ['HOME']
    file_path = os.path.join(home, ".config.fifth_elephant")
    print("home:", file_path)

    with open(file_path, 'r') as f:
        raw = f.read()

    secrets = json.loads(raw)
    if secrets is None:
        print("Failed to parse config file!")
        os.sys.exit(-1)

    our_client_id = secrets[instance]["client_id"]
    our_client_secret = secrets[instance]["client_secret"]
    our_access_token = secrets[instance]["access_token"]
    return Mastodon(client_id=our_client_id,
                    client_secret=our_client_secret, access_token=our_access_token)


def save(instance, toots):
    """
    Pickles toots
    Args:
        instance - used to identify pickles
        toots - to be pickled
    """
    file_path = os.path.join(".", "dontcommitmebro", instance + "toots.pickle")
    with open(file_path, "wb") as f:
        pickle.dump(toots, f)

    print("cached toots for", instance)


def setup(instance):
    mastodon = init(instance)
    data = mastodon.timeline_local(limit=25)
    save(instance, data)


def load(instance):
    """
    Unpickles toots
    Args: instance - to load
    Returns: toots
    """
    file_path = os.path.join(".", "dontcommitmebro", instance + "toots.pickle")
    with open(file_path, "rb") as f:
        return pickle.load(f)


def display_toots(instance):
    toots = load(instance)
    print("no of toots: {}\n\n".format(len(toots)))
    for toot in toots:
        # print(json.dumps(toot))
        print("  {}  @{} {}".format(toot['account']['display_name'],
                                    toot['account']['username'],
                                    toot['created_at']))

        if toot['application'] is None:
            application = ''
        else:
            application = "via {}".format(toot['application']['name'])

        print("  ♺::{} ♥:{} id:{} {}".format(toot['reblogs_count'],
                                             toot['favourites_count'],
                                             toot['id'],
                                             application))

        soup = BeautifulSoup(toot['content'], "html.parser")
        toot_text = soup.get_text()
        print("  {} - {}\n".format(toot_text,
                                   toot['url']))


if __name__ == '__main__':
    instance = "icosahedron.website"
    # instance = "witches.town"
    setup(instance)

    instance = "icosahedron.website"
    print("toots for", instance)
    display_toots(instance)

    # print("//////////////////////////////////////////////////////////////////")


    # toots = load(instance)
    # print("no of toots: {}\n\n".format(len(toots)))

    # instance = "witches.town"
    # print("toots for", instance)
    # display_toots(instance)
