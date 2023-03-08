reinstall_package:
	@pip uninstall -y sensuous || :
	@pip install -e .
