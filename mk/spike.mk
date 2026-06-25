SPIKE_SRC := $(ROOT_DIR)/third_party/spike
SPIKE_BUILD := $(ROOT_DIR)/build/spike

.PHONY: spike
spike: $(SPIKE_BUILD)/Makefile
	$(MAKE) -C $(SPIKE_BUILD)

$(SPIKE_BUILD)/Makefile: $(SPIKE_SRC)/configure
	mkdir -p $(SPIKE_BUILD)
	cd $(SPIKE_BUILD) && $(SPIKE_SRC)/configure --prefix=$(SPIKE_BUILD)/install

.PHONY: clean-spike
clean-spike:
	rm -rf $(SPIKE_BUILD)