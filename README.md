## Persenal repo

### env:

    python3.8.20
    cadquery
    scipy
    

### dir discribe:

    CADQuery:                forget,maybe test
    Gen:                     generate CADQuery from raw_data
    Gen_CADquery:            CADQuery from Gen
    OUTPUT_for_check:        run CADQuery produce .stl/.step
    


### sample_data_format:

    sample_data = {
    
    "V0":{

        "M":[                                   # 4*4变换矩阵
            [           , T ],
            [     R     , T ],
            [           , T ],
            [ 0 , 0 , 0 , 1 ]
        ],

        "is_solid": True,                       #实体或槽/孔结构，实体为True
        "Profile": {                            #截面曲线
            "X0": [0, 0],  # 顶点坐标不变
            "0E1": {       # 边定义改为字典
                "type": "line",           # 直线
            },

            "X1": [100, 0], 
            "1E2": {
                "type": "circular_arc",   # 圆弧
                "origin": [x, y],         # 圆心坐标
                "angle": 1.57,            # 弧度制角度（正=逆时针）
                "origin": [x, y],         # 圆心坐标
            },

            "X2":[*,*],
            "2E3": {
                "type": "elliptical_arc", # 椭圆弧
                "major_radius": 100,      # 长轴
                "minor_radius": 50,       # 短轴
                "origin": [x, y],         # 椭圆圆心坐标
                "start_angle": 0,         # 起始角度（弧度）
                "end_angle": 1.57,        # 终止角度
                "dx": [x,y]               # 长轴方向向量
                "clocksign": 1/-1         # 1为逆  -1为顺
            }
        },        
        "Path": {                               #扫掠路径
            "P0": [0, 0, 0], "0E1": 0,"0N1": [0,0,0],           #   P：三维点坐标
            "P1": [0, 0, 200]                                   #   mNn：从m点到n点的圆弧的弦中点指向圆心的三维法向量
        }        
    },
    
    "V1":{                                                      #   对于不同的Vi，统一通过M控制相对位置

        "M":[                                   # 4*4变换矩阵
            [           , T ],
            [     R     , T ],
            [           , T ],
            [ 0 , 0 , 0 , 1 ]
        ],                                    #   在旋转后的坐标系中按照二维点坐标绘制截面并扫掠生成Vi
        "is_solid": False,
        "Profile": {
            "X0":[20, 20], 
            "0E1":{
                "type": "circular_arc",   # 圆弧
                "origin": [x, y],         # 圆心坐标
                "angle": 3.14,            # 弧度制角度（正=逆时针）
                "origin": [x, y],         # 圆心坐标
            },
            "X1":[50, 50], 
            "1E0":{
                "type": "circular_arc",   # 圆弧
                "origin": [x, y],         # 圆心坐标
                "angle": 3.14,            # 弧度制角度（正=逆时针）
                "origin": [x, y],         # 圆心坐标
            }, 
        },
        "Path": {
            "P0": [0, 0, 0], "0E1": 0,"0N1": [0,0,0],
            "P1": [0, 0, -200]
        }
    },
    
    "V2":{

        "M":[                                   # 4*4变换矩阵
            [           , T ],
            [     R     , T ],
            [           , T ],
            [ 0 , 0 , 0 , 1 ]
        ],
        "is_solid": False,
        "Profile": {
            "X0":[20, 20], 
            "0E1":{
                "type": "circular_arc",   # 圆弧
                "origin": [x, y],         # 圆心坐标
                "angle": 3.14,            # 弧度制角度（正=逆时针）
                "origin": [x, y],         # 圆心坐标
            },
            "X1":[50, 50], 
            "1E0":{
                "type": "circular_arc",   # 圆弧
                "origin": [x, y],         # 圆心坐标
                "angle": 3.14,            # 弧度制角度（正=逆时针）
                "origin": [x, y],         # 圆心坐标
            }, 
        },
        "Path": {
            "P0": [0, 0, 0], "0E1": 0,"0N1": [0,0,0],
            "P1": [0, 0, -100]
        }
    }
}