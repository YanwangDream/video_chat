import streamlit as st

import requests
import json


# 定义获取access_token的函数
def get_access_token(api_key, secret_key):
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    response = requests.post(url)
    return response.json().get("access_token")


# 定义发送消息到API的函数
def send_message_to_api(access_token, messages, max_output_tokens, temperature, role):
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token={access_token}"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers,
                             data=json.dumps(
                                 {"messages": messages, "max_output_tokens": max_output_tokens,
                                  "temperature": temperature, "system": role}))
    return response.json()


# 用于处理Streamlit页面逻辑
def main():
    # 创建Streamlit网页元素
    st.title('提示工程集成助手之视频脚本生成')
    st.write('<p style="color:grey; font-size:14px;">这里是提示语输入的地方😎😎😎😎😎😎</p>',
             unsafe_allow_html=True)

    # 在侧边栏添加输入框用于输入API Key和Secret Key
    # api_key = st.sidebar.text_input('请输入API Key：')
    # secret_key = st.sidebar.text_input('请输入Secret Key：')
    with st.sidebar:
        api_key = st.text_input('请输入API Key：', type="password")
        secret_key = st.text_input('请输入Secret Key：', type="password")
        st.markdown("[获取文心一言 API Key和Secret Key](https://console.bce.baidu.com/)")

    # # 在侧边栏添加一个确认按钮
    # if st.sidebar.button('确认'):
    #     # 在这里执行一些操作，比如验证API凭据或者重新运行应用
    #     # 例如，你可以打印出输入的API凭据来确认它们已经被输入
    #     st.write("API Key:", api_key)
    #     st.write("Secret Key:", secret_key)

    # 检查API Key和Secret Key是否为空
    if not api_key or not secret_key:
        st.warning('请确保API Key和Secret Key都已填写！')
        return

    # 获取access_token
    access_token = get_access_token(api_key, secret_key)

    # 使用两列布局
    left_column, right_column = st.columns(2)

    # 在左侧列中添加五个输入框
    with left_column:
        role = st.text_input('这个固定填写是角色，别改成填写其他的了哈👀👀', key='input0')
        user_input1 = "请根据主题生成短视频脚本要求紧贴主题，我的主题为" + st.text_input('视频主题：', key='input1')
        user_input2 = "内容长度需要紧扣时长且短视频时长为" + st.text_input('短视频时长为：', key='input2')
        user_input3 = "根据要求在内容中需要具备" + st.text_input('根据要求在内容中需要具备：', key='input3')
        user_input4 = "内容需要侧重于" + st.text_input('内容需要侧重于：', key='input4')
        user_input5 = "需要贴近平台用户群体、视频长度、内容风格确保你的脚本与平台特点相匹配，投放平台为" + st.text_input('投放平台为（或输入"exit"退出）：', key='input5')
        # 衔接词加载衔接词的框里不需要则删除（自由选择），题目就是“内容自己定”，不要就删除几个

    # 在右侧列中添加一个输入框，并尽量使其高度与左侧一致
    with right_column:
        right_input = st.text_input('这里提示要放提示模板：', key='right_input')
        max_output_tokens = st.slider("输出最大Token数", min_value=2,
                                      max_value=4096, value=500, step=1)
        temperature = st.slider("丰富性，较高的数值会使输出更加随机", min_value=0.1,
                                max_value=1.0, value=0.95, step=0.05)

    # 检查用户是否想要退出
    if user_input5.lower() == 'exit':
        st.write("退出程序。")
        return

    # 组合用户输入
    combined_user_input = " ".join(
        [user_input1, user_input2, user_input3, user_input4, user_input5, right_input]).strip()

    messages = [{"role": "user", "content": combined_user_input}]

    submit=st.button('显示机器人回复')

    if access_token is None and submit:
        st.write("API返回错误!请重新输入")
        return
    if access_token is not None and not role and submit:
        st.write("请填写角色和相应的内容，否则会输入意想不到的事情！")
        return

    if access_token is not None and submit:
        with st.spinner("AI正在思考中，请稍等..."):
            response = send_message_to_api(access_token, messages, max_output_tokens, temperature, role)
            if 'result' in response:
                robot_response = response['result']
                # 定义一个按钮，点击后执行下面的代码块
                # if st.button('显示机器人回复'):
                #     st.write("机器人回复:", robot_response)
                st.write("机器人回复:", robot_response)

    # 处理API响应
    # if 'error_code' in response:
    #     st.write("API返回错误:", response)
    # else:
    #     # 提取并打印机器人的响应
    #     if 'result' in response:
    #         robot_response = response['result']
    #         # 定义一个按钮，点击后执行下面的代码块
    #         if st.button('显示机器人回复'):
    #             st.write("机器人回复:", robot_response)


if __name__ == '__main__':
    main()
