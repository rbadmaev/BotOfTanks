# API

Бот будет отдельным приложением, которое читает из `stdin` и пишет в `stdout`.
Чтение производится построчно. Т.е. каждая строка - это отдельное сообщение.
При старте приложения, до чтения первого сообщение оно должно первой строкой вывести название бота.
Сообщения в формате JSON.

## Входящее сообщение
Входящее сообщение содержит полное описание текущего состояния игры.
- Каждый танк описывается следующим json сообщением
    ```json
    {
        "position": [int_x, int_y],
        "radius": int_radius,
        "movement": [double_x, double_y],
        "move_forward": bool,
        "max_acceleration": double_acceleration,
        "canon_angle": double_angle,
        "canon_rotate_speed": double_angle_per_time_quant,
        "health": int_health,
    }
    ```
- Каждый снаряд описывается следующим сообщением
    ```json
    {
        "position": [int_x, int_y],
        "movement": [double_x, double_y]
    }
    ```

Полный формат входящего сообщения тогда будет таким
```json
{
    "map_size": [int_x_size, int_y_size],
    "me": {
        "position": [int_x, int_y],
        "radius": int_radius,
        "movement": [double_x, double_y],
        "max_acceleration": double_acceleration,
        "canon_angle": double_angle,
        "canon_rotate_speed": double_angle_per_time_quant,
        "health": int_health
    },
    "enemies": [
        {
            "position": [int_x, int_y],
            "radius": int_radius,
            "movement": [double_x, double_y],
            "max_acceleration": double_acceleration,
            "canon_angle": double_angle,
            "canon_rotate_speed": double_angle_per_time_quant,
            "health": int_health
        },
        ...
    ],
    "bullets": [
        {
            "position": [int_x, int_y],
            "movement": [double_x, double_y]
        },
        ...
    ]
}
```

## Исходящее сообщение
Исходящее сообщение содержит гораздо меньше информации
```json
{
    "acceleration": [double_x, double_y],
    "canon_rotate_to": double_target_canon_angle,
    "shoot": bool_need_to_shoot
}
```
