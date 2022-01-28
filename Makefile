
APPS = laketemp
.PHONY: release $(APPS)

release: $(APPS)

$(APPS):
	gcloud functions deploy $@ --source=$@

test:
	echo foo
