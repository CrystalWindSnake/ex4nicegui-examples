import provider


def word(en: str, zh: str):
    return lambda: en if provider.language.get().value == "en" else zh


class Translates:
    app_title = word("Todo List", "待办事项列表")
    add_task_input_placeholder = word("Add a new task", "添加任务")
    filter_type_all = word("all", "全部")
    filter_type_active = word("active", "进行中")
    filter_type_completed = word("completed", "已完成")

    filter_label = word("item(s) left", "事项")

    items_table_header_check = word("Status", "状态")
    items_table_header_title = word("Title", "标题")
    items_table_header_priority = word("Priority", "优先级")
    items_table_header_delete = word("Delete", "删除")

    todo_item_del_tooltip = word(
        "only completed items can be deleted", "已完成的事项才可以删除"
    )

    clear_completed_button_text = word("Clear completed", "清除所有已完成事项")

    statistics_card_title = word("statistics", "数据统计")

    statistics_card_completed_text = word("completed todos", "已完成事项")
    statistics_card_active_text = word("active todos", "进行中事项")
    statistics_card_total_text = word("total items", "总事项")

    statistics_card_text_tooltip = word("click to view", "点击查看")
