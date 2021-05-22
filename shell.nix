let
  pkgs = import <nixpkgs> {};
in

with pkgs;
with stdenv;

mkDerivation rec {
  name = "magical-zilch-specification";
  version = "0.0.1";

  buildInputs = [
    gnumake
    texlive.combined.scheme-full
    python38Packages.pygments
  ];
}
