import random
import nodes
from gatcha_items import gatcha_items


def draw_lottery():
    item_name_list = []
    weight_list = []
    for k, item in gatcha_items.items():
        item_name_list.append(item['name'])
        weight_list.append(item['ratio'])

    item = random.choices(item_name_list, weight_list)[0]
    return item


def gatcha(turn_times):
    if turn_times == 1:
        draw_lottery()
    if turn_times == 10:
        pass


def change_node(node_key, accept):
    if node_key == 'launch':
        return 'welcome'
    elif node_key == 'welcome':
        return 'gatcha' if accept else 'recommend'
    elif node_key == 'recommend':
        return 'gatcha' if accept else 'end'
    elif node_key == 'gatcha':
        return 'gatcha' if accept else 'end'


def should_gatcha(turn_times):
    return bool(turn_times)


def main(alexa_user_id, turn_times, node_key):
    action = {'type': 'ganesha'}

    if node_key == 'launch':
        node = nodes.launch()
    elif node_key == 'welcome':
        if should_gatcha(turn_times):
            node = nodes.gatcha(turn_times)
        else:
            node = nodes.recommend()
    elif node_key == 'recommend':
        if should_gatcha(turn_times):
            node = nodes.gatcha(turn_times)
        else:
            node = nodes.end()
    elif node_key == 'gatcha':
        if should_gatcha(turn_times):
            node = nodes.gatcha(turn_times)
        else:
            node = nodes.end()
    else:
        node = {
            'original_texts': [
                {
                    'text': ''
                }
            ]
        }

    # nodeのturn_timesを優先する。
    accept = bool(node.get('turn_times', turn_times))
    node['node'] = change_node(node_key, accept)

    action.update(node)

    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    turn_times = event.get('turn_times')
    node_key = event.get('node', 'launch')
    response = main(alexa_user_id, turn_times, node_key)
    return response
