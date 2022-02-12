#!/usr/bin/env python
# -*- coding:utf-8 -*-
import uvicorn


def main() -> None:
    kwargs = {
        "app": "backend.http.api:app",
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,
    }
    uvicorn.run(**kwargs)
    return


if __name__ == '__main__':
    main()
