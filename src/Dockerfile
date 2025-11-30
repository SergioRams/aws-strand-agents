FROM public.ecr.aws/lambda/python:3.12

# Install tar and xz to extract the static build
RUN dnf install -y tar xz && \
    dnf clean all

# Download FFmpeg static build
RUN curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o ffmpeg.tar.xz && \
    tar -xf ffmpeg.tar.xz && \
    # Move binaries to /usr/local/bin so they are in PATH
    mv ffmpeg-*-amd64-static/ffmpeg /usr/local/bin/ && \
    mv ffmpeg-*-amd64-static/ffprobe /usr/local/bin/ && \
    # Cleanup
    rm -rf ffmpeg.tar.xz ffmpeg-*-amd64-static

# Copy requirements
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install Python dependencies
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]
