%define vendor_name Intel
%define vendor_label intel
%define driver_name fm10k

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 0.26.1
Release: 1%{?dist}
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-intel-fm10k/archive?at=0.26.1&format=tgz&prefix=driver-intel-fm10k-0.26.1#/intel-fm10k-0.26.1.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-intel-fm10k/archive?at=0.26.1&format=tgz&prefix=driver-intel-fm10k-0.26.1#/intel-fm10k-0.26.1.tar.gz) = 96bc082a0a57cbb73400a27260764137af99c756


BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true KERNELVERSION=%{kernel_version} modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
