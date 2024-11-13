FROM python:3.10-slim as base

# ---- 构建依赖阶段 ----
FROM base AS requirements

WORKDIR /src

RUN RUN python -m pip install -U poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry export -f requirements.txt --without-hashes -o /src/requirements.txt
# install app dependencies
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# ---- 生产环境阶段 ----
FROM base AS production

LABEL MAINTAINER="Wenbao Xu<xu-wenbao@foxmail.com>"

WORKDIR /src

COPY . .
COPY --from=requirements /src/requirements.txt .
COPY --from=requirements /root/.cache /root/.cache

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
    && rm -rf /root/.cache

EXPOSE 7860

CMD ["uvicorn", "fastapi_demo.main:app", "--workers", "2",  "--host", "0.0.0.0", "--port", "7860"]
