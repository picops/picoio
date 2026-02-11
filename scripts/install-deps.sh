# Install g++
if ! command -v g++ &> /dev/null; then
    echo "g++ not found. Installing build-essential..."
    sudo apt-get update
    sudo apt-get install -y build-essential
else
    echo "g++ is already installed."
fi

# Install cmake
if ! command -v cmake &> /dev/null; then
    echo "cmake not found. Installing cmake..."
    sudo apt-get install -y cmake
else
    echo "cmake is already installed."
fi

# Install libzmq3-dev 
if ! dpkg -s libzmq3-dev &> /dev/null; then
    echo "libzmq3-dev not found. Installing libzmq3-dev..."
    sudo apt-get install -y libzmq3-dev
else
    echo "libzmq3-dev is already installed."
fi

# Install libzip-dev
if ! dpkg -s libzip-dev &> /dev/null; then
    echo "libzip-dev not found. Installing libzip-dev..."
    sudo apt-get install -y libzip-dev
else
    echo "libzip-dev is already installed."
fi  

# Install pybind11
if ! dpkg -s pybind11-dev &> /dev/null; then
    echo "pybind11 not found. Installing pybind11..."
    sudo apt-get install -y pybind11-dev
else
    echo "pybind11 is already installed."
fi

# Check if Arrow APT repo is installed; if not, install it
if ! grep -q "apache-arrow" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
    echo "Apache Arrow APT repository not found. Installing Arrow APT repo..."
    sudo apt-get update
    sudo apt-get install -y wget lsb-release
    ARROW_DEB="apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb"
    wget https://apache.jfrog.io/artifactory/arrow/$(lsb_release --id --short | tr 'A-Z' 'a-z')/${ARROW_DEB}
    sudo apt install -y -V ./${ARROW_DEB}
    rm -f ./${ARROW_DEB}
    sudo apt update
else
    echo "Apache Arrow APT repository is already installed."
fi
# Install libarrow-dev
if ! dpkg -s libarrow-dev &> /dev/null; then
    echo "libarrow-dev not found. Installing libarrow-dev..."
    sudo apt install -y -V \
        libarrow-dev \
        libarrow-glib-dev \
        libarrow-dataset-dev \
        libarrow-dataset-glib-dev \
        libarrow-acero-dev \
        libarrow-flight-dev \
        libarrow-flight-glib-dev \
        libarrow-flight-sql-dev \
        libarrow-flight-sql-glib-dev \
        libgandiva-dev \
        libgandiva-glib-dev \
        libparquet-dev \
        libparquet-glib-dev
else
    echo "libarrow-dev is already installed."
fi



