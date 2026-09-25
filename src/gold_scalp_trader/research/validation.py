def non_overlapping(train_end:int,validation_start:int,validation_end:int,holdout_start:int)->bool:return train_end<=validation_start<validation_end<=holdout_start
