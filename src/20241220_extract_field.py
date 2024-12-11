import re
from typing import List


# 通用提取函数：基于关键词和规则提取内容
def extract_field(content: str, key: str, length: int = 25, pattern: str = r'[A-Za-z0-9]+'):
    """从内容中提取基于关键字和规则的字段"""
    start = content.find(key)
    if start != -1:
        section = content[start + len(key): start + len(key) + length]
        match = re.search(pattern, section)
        return match.group(0) if match else ''
    return ''


# 提取相邻内容
def extract_near_content(content: str, key: str, length: int, before: bool = True):
    """提取关键字前后固定长度的内容"""
    position = content.find(key)
    if position == -1:
        return ''

    start = position - length if before else position + len(key)
    end = position if before else position + len(key) + length
    return content[max(0, start):end]


# 提取数字
def extract_num(content: str):
    """提取第一个出现的数字"""
    match = re.search(r'\d+', content)
    return match.group(0) if match else ''


# 主函数：根据规则提取数据
def extract_fields(data: List[str]):
    """根据规则提取目标字段"""
    content = ''.join(data)  # 将列表合并为单一字符串
    keys = {
        'car_company_name': '车辆生产企业名称',
        'car_vin': '车辆识别代号',
        'car_model_name': '车型名称',
        'car_model': '车辆型号',
        'car_brand': '车辆品牌(中文/英文)',
        'car_color': '车辆颜色',
        'engine_number': '发动机编号',
        'engine_model': '发动机型号/燃料种类',
        'max_power': '排量(ml)/最大净功率(kW)',
        'axles_num': '车轴数量',
        'wheels_num': '车轮数量',
        'wheel_width': '轮距(mm)',
        'overall_size': '外廓尺寸(长/宽/高mm)',
        'track_width': '轴距(mm)',
        'curb_weight': '整备质量(kg)',
        'max_weight': '最大允许总质量(kg)',
        'tire_size': '轮胎规格型号'
    }
    extracted_data = {key: next((data[i + 1] for i, item in enumerate(data) if value in item), '') for key, value in
                      keys.items()}

    # 特殊字段的额外规则处理
    extracted_data['max_speed'] = extract_num(extract_near_content(content, '最高设计车速', length=20, before=False) or "")
    extracted_data['passenger_capacity'] = extract_num(extract_near_content(content, '额定载客人数', length=50,
                                                                           before=False) or "")

    return extracted_data


# 测试数据
sample_data = ['强制性产品认证车辆一致性证书', '车辆致性证书', '编号', 'V000206HBBRV000206HHBREDQY4Q0528570R1700100B0', '基本车辆制造国', '美国', '最终阶段车辆制造国', '美国', '车辆生产企业名称', '和合加利福尼亚汽车集团公司', '车辆生产企业地址', '美国加州圣伯纳迪诺县奇诺市中央大街14144号B单元', '委托人名称', '福建晟圆汽车发展有限公司', '生产者(制造商)名称', '和合加利福尼亚汽车集团公司', '新能源车', '否', '产品标牌的位置', '副驾驶右侧B柱', '车辆识别代号', '1FMEE5DP9NLB41601', '车辆识别代号打刻位置', '副驾驶下方纵梁上', '越野乘用车(福特平行进', '车型名称', '车辆型号', 'BRONCO 2.7', '11)(5座)', '车辆注册类型', '小型越野客车', '车辆类别', 'MIG', '克罗迪', '列', '马', '车辆品牌(中文/英文)', '车辆颜色', '黄', 'QUALITYNE BRONCO)', '发动机编号', 'NLB41601P', '发动机编号在发动机上的打刻位置', '发动机缸体上', '车型种类', '完整车辆', '基本车辆一', '一致性证书编号', 'V000206HIIBREDQY4Q0528570R1700100', '基本车辆型号', '基本车辆类别', '整车', '最终(或本)阶段车辆CCC证书编号(版本号)/签发日期', '2022221101000119(B0)/2022-06-01', '车轴数量', '2', '车轮数量', '4', '驱动轴位置', '前轴/后轴', '前悬(mm)/后悬(mm)', '850/1050', '轮距', '(mm)', '1655', '外廓尺寸(mm)', '4855/1960/1880', '轴距)', '2955', '货厢内部尺寸(mm)', '额定载客人数', '5', '接近角/离去角(°', ')', '35.6/38.3', '整备质量(kg)', '2210', '额定载质量(kg)', '不适用', '载质量利用系数', '车门数量和结构', '5/铰接', '最大允许总质量(kg)', '2803', '最人允许总质量对应的轴荷分配(kg)', '1445/1358', '车辆最前端与牵引装置中心之间的距离(mm)', '车辆是否适合拖挂', '最大允许牵引质量(kg)', '直接喷射', '否', '发动机型号/燃料种类', 'P/汽油', '气缸数量和排列', '6/V列', '排量(ml)/最人净功率(kW)', '2694/246', '离合器(型式)', '多片湿式', '变速器(型式)', '自动', '转向形式', '方向盘式', '最高设计车速(km/h)', '160', '轮胎规格型号', '车轴1：LT285/70R17：车轴2：LT285/70R17；', '制动装置简要说明', '盘式制动', '驱动轴是否装空气悬挂或等效装置', '驾驶室准乘人数', '5是', '牵引车与挂车的最大组合质量(kg)', '是否带防抱死系统', '牵引车与挂车连接点处最大重直质量(kg', '/', '4.714/2.997/2.149/1.769/1.521/1.275/1，000/0.853/0.689/0.636', '速比', '本', '丰传动比', '4.10', '倒档：4.885', '钢板弹簧片数(片)', '车辆制造日期', '2022306', 'CCC认证所依据标准的编号及对应的实施阶段', 'GB1495-2002，GB/T14365-2017', '声级', '定置噪声(dB(A))', '79', '加速行驶车外噪声(dB(A))', '70.0', 'CCC认证所依据标准的编号及对应的实施阶段', 'GB18352.62016', '排气污', 'CO', '740', 'THC', '5', '试验用液体', '染物', 'NOx', '50', 'AMHC', '燃料：', '烟度(吸收系数(m-1)的校正值)', '不适用', '微粒物/PN', '3.0/6.0×1011', 'CCC认证所依据标准的编号', 'GB18352.6-2016：GB/T19233-2020', 'C02排放量', '燃料消耗量', '低速段(g/km)', '405.26', '低速段(L/100km)', '17.00', 'C02排放量/燃料消耗量', '中速段(g/km)', '258.42', '中速段(L/100km)', '10.82', '高速段(g/km)', '231.39', '高速段(L/100km)', '9.68', '超高速段(g/km)', '279.19', '超高速段(L/100km)', '11.69', 'WLTC综合(g/km', '277.00', 'WLTC综合(L/100km)', '11.60', '委托人联系方式', '联系人', '李盈', '联系电话', '15698851050', '备注', 'VIN第十位年份代码采用车型年份，并日符合GB16735-2019标准要求', 'C', '28']

# 运行提取函数并打印结果
result = extract_fields(sample_data)
for key, value in result.items():
    print(f"{key}: {value}")
