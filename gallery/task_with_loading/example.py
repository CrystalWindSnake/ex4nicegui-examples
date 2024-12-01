from ex4nicegui import rxui, to_ref
from nicegui import ui
import asyncio
from core import LoadingTaskManager


@ui.page("/")
async def main():
    # 数据状态
    # ui state

    ## 虽然这些数据需要耗时计算，但你还是需要给一个初始值
    ## you still need to provide an initial value for these data
    text_input = to_ref("")
    table_data = to_ref([])

    # 定义了耗时计算后，把需要的数据更新
    # define the data that needs to be updated after the time-consuming calculation
    @LoadingTaskManager
    async def data_a_task():
        await asyncio.sleep(2)
        text_input.value = "hello"
        table_data.value = [1, 2, 3]

    # ui
    ui.label("耗时任务等待示例")
    ui.label("long time task waiting example")

    @data_a_task.view
    def _():
        rxui.input(value=text_input)
        rxui.label(f"{table_data.value=}")

    ui.label("其他内容")
    ui.label("other content")


ui.run()
