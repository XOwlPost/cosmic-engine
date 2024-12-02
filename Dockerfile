FROM ubuntu:22.04

# Install required build tools
RUN apt-get update && apt-get install -y \
    build-essential wget gcc g++ make bison gawk python3 && \
    apt-get clean

# Set working directory
WORKDIR /tmp

# Download and build GLIBC
RUN wget http://ftp.gnu.org/gnu/libc/glibc-2.38.tar.gz && \
    tar -xvzf glibc-2.38.tar.gz && \
    cd glibc-2.38 && \
    mkdir build && cd build && \
    ../configure --prefix=/opt/glibc-2.38 && \
    make -j$(nproc) && \
    make install && \
    cd /tmp && rm -rf glibc-2.38*

# Provide bash for interaction
CMD ["bash"]
