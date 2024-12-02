FROM ubuntu:22.04

# Install necessary build tools
RUN apt-get update && apt-get install -y \
    build-essential wget gcc g++ \
    && apt-get clean

# Download and build GLIBC
WORKDIR /tmp
RUN wget http://ftp.gnu.org/gnu/libc/glibc-2.38.tar.gz && \
    tar -xvzf glibc-2.38.tar.gz && \
    cd glibc-2.38 && \
    mkdir build && cd build && \
    ../configure --prefix=/opt/glibc-2.38 && \
    make -j$(nproc) && \
    make install

# Clean up
RUN rm -rf /tmp/glibc-2.38*

# Provide bash by default
CMD ["bash"]
