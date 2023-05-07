from typing import Dict, Any, List


def dict2str(data: Any | Dict[Any, Any], enclose: bool = False):
    result: str = ""
    if isinstance(data, dict):
        parts: List[str] = []
        for key, value in data.items():
            if not isinstance(key, str) or len(key) == 0 or value is None:
                continue
            elif value == "":
                if key[0] == "`":
                    parts.append(key[1:])
                else:
                    parts.append(key)
            else:
                new_value: str = dict2str(value, True)
                if new_value == "{}":
                    continue
                parts.append(f"{key}={new_value}")
        result = ",".join(parts)
    else:
        result = str(data)
    return f"{{{result}}}" if enclose else f"{result}"


print(dict2str({"si": "width", "r": None, "R": "", "inner": {"a": 5, "b": 6}}))
print(dict2str({"si": "width", "r": None, "R": "", "inner": {"a": None, "b": None}}))
print(
    dict2str(
        {
            "si": "width",
            "r": None,
            "R": "",
            "inner": {"a": None, "b": None},
            "`inner": "",
        }
    )
)
