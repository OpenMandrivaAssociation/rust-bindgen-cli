# Rust packages always list license files and docs
# inside the crate as well as the containing directory
%undefine _duplicate_files_terminate_build
%bcond_without check

%global crate bindgen-cli

Name:           rust-bindgen-cli
Version:        0.69.4
Release:        1
Summary:        Automatically generates Rust FFI bindings to C and C++ libraries
Group:          Development/Rust

License:        BSD-3-Clause
URL:            https://crates.io/crates/bindgen-cli
Source:         %{crates_source}
Source1:	vendor.tar.xz

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  rust >= 1.64.0

%global _description %{expand:
Automatically generates Rust FFI bindings to C and C++ libraries.}

%description %{_description}

%files
%license LICENSE
%license LICENSE.dependencies
%doc README.md
%{_bindir}/bindgen

%prep
%autosetup -n %{crate}-%{version} -p1 -a1
%cargo_prep
cat >.cargo/config.toml <<EOF
[profile.rpm]
inherits = "release"
opt-level = 3
codegen-units = 1
debug = 2
strip = "none"

[env]
CFLAGS = "%{build_cflags}"
CXXFLAGS = "%{build_cxxflags}"
LDFLAGS = "%{build_ldflags}"

[install]
root = "%{buildroot}%{_prefix}"

[term]
verbose = true

[net]
offline = true

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
%cargo_install

%if %{with check}
%check
%cargo_test
%endif
