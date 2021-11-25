let
  pkgs = import <nixpkgs> {};

  railroad = with pkgs.python38Packages;
    buildPythonPackage rec {
      pname = "railroad-diagrams";
      version = "1.1.1";

      src = fetchPypi {
        inherit pname version;
        sha256 = "0xn9chq3nqyjj38f9akpc1cg31vryx0afjkrfq701qkbcqkw47la";
      };
    };
in
with pkgs;

mkShell rec {
  name = "railroad-diagram-generator";
  version = "1.0.0";

  buildInputs = [
    (python38.withPackages (_: [ railroad ]))
  ];
}
