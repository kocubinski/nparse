from PyQt5.QtWidgets import (QMessageBox, QInputDialog, QDialog,
                             QCheckBox, QSpinBox, QColorDialog)
from PyQt5 import uic
from PyQt5.QtCore import Qt

from helpers import config, resource_path, set_qcolor, get_rgb
from .triggers import TriggerTree
from .triggereditor import TriggerEditor


class SettingsWindow(QDialog):

    def __init__(self):
        super().__init__()

        uic.loadUi(resource_path('data/ui/settings.ui'), self)

        self._ref = {}
        self._ref = self._build_ref()

        # events
        self.addTriggerButton.clicked.connect(self._addTrigger)
        self.newGroupButton.clicked.connect(self._addGroup)
        self.removeButton.clicked.connect(self._removeItem)

        # color button events
        self.buffTextColorButton.clicked.connect(self._set_buff_text_color)
        self.buffBarColorButton.clicked.connect(self._set_buff_bar_color)
        self.debuffTextColorButton.clicked.connect(self._set_debuff_text_color)
        self.debuffBarColorButton.clicked.connect(self._set_debuff_bar_color)
        self.youColorButton.clicked.connect(self._set_you_color)
        self.friendlyColorButton.clicked.connect(self._set_friendly_color)
        self.enemyColorButton.clicked.connect(self._set_enemy_color)
        self.targetTextColorButton.clicked.connect(self._set_target_text_color)

    def _set_buff_text_color(self, _):
        cd = QColorDialog(parent=self)
        color = cd.getColor()
        set_qcolor(
            self.buffBarLabel,
            foreground=color.getRgb()
        )
        cd.setParent(None)

    def _set_buff_bar_color(self, _):
        cd = QColorDialog(parent=self) 
        color = cd.getColor()
        set_qcolor(
            self.buffBarLabel,
            background=color.getRgb()
        )
        cd.setParent(None)

    def _set_debuff_text_color(self, _):
        cd = QColorDialog(parent=self) 
        color = cd.getColor()
        set_qcolor(
            self.debuffBarLabel,
            foreground=color.getRgb()
        )
        cd.setParent(None)

    def _set_debuff_bar_color(self, _):
        cd = QColorDialog(parent=self) 
        color = cd.getColor()
        set_qcolor(
            self.debuffBarLabel,
            background=color.getRgb()
        )
        cd.setParent(None)
    
    def _set_you_color(self, _):
        cd = QColorDialog(parent=self)
        color = cd.getColor()
        set_qcolor(
            self.youTargetLabel,
            background=color.getRgb()
        )
        cd.setParent(None)

    def _set_friendly_color(self, _):
        cd = QColorDialog(parent=self)
        color = cd.getColor()
        set_qcolor(
            self.friendlyTargetLabel,
            background=color.getRgb()
        )
        cd.setParent(None)

    def _set_enemy_color(self, _):
        cd = QColorDialog(parent=self)
        color = cd.getColor()
        set_qcolor(
            self.enemyTargetLabel,
            background=color.getRgb()
        )
        cd.setParent(None)
    
    def _set_target_text_color(self, _):
        cd = QColorDialog(parent=self)
        color = cd.getColor()
        set_qcolor(
            self.youTargetLabel,
            foreground=color.getRgb()
        )
        set_qcolor(
            self.friendlyTargetLabel,
            foreground=color.getRgb()
        )
        set_qcolor(
            self.enemyTargetLabel,
            foreground=color.getRgb()
        )
        cd.setParent(None)

    def _addTrigger(self, _):
        text, response = QInputDialog.getText(
            self,
            "New Trigger",
            "Enter Trigger Name:"
        )
        if response:
            if not self.triggerTree.trigger_exists(text):
                self.triggerTree.add_new_trigger(text)

    def _addGroup(self, _=None):
        text, response = QInputDialog.getText(
            self,
            "New Group",
            "Enter New Group Name:"
        )
        if response:
            if not self.triggerTree.group_exists(text):
                self.triggerTree.add_new_group(text)
            else:
                QMessageBox(
                    QMessageBox.Warning,
                    "Warning", "{} group already exists.".format(text),
                    QMessageBox.Ok
                ).exec()
                self._addGroup()

    def _removeItem(self, _=None):
        if self.triggerTree.is_group_selected():
            r = QMessageBox.question(
                self,
                "Are you sure?",
                "Selected item is a group.  Remove group and all triggers it contains?"
            )
            if r == QMessageBox.No:
                return
        self.triggerTree.remove_selected()

    def save_settings(self):
        for section, references in self._ref.items():
            for setting, widget in references.items():
                wt = type(widget)
                if wt == QCheckBox:
                    config.data[section][setting] = widget.isChecked()
                    widget.setChecked(config.data[section][setting])
                elif wt == QSpinBox:
                    config.data[section][setting] = widget.value()
                    widget.setValue(config.data[section][setting])
        #spell color bars
        config.data['spells']['buff_text_color'] = get_rgb(self.buffBarLabel, self.buffBarLabel.foregroundRole())
        config.data['spells']['buff_bar_color'] = get_rgb(self.buffBarLabel, self.buffBarLabel.backgroundRole())
        config.data['spells']['debuff_text_color'] = get_rgb(self.debuffBarLabel, self.debuffBarLabel.foregroundRole())
        config.data['spells']['debuff_bar_color'] = get_rgb(self.debuffBarLabel, self.debuffBarLabel.backgroundRole())
        config.data['spells']['you_target_color'] = get_rgb(self.youTargetLabel, self.youTargetLabel.backgroundRole())
        config.data['spells']['friendly_target_color'] = get_rgb(self.friendlyTargetLabel, self.friendlyTargetLabel.backgroundRole())
        config.data['spells']['enemy_target_color'] = get_rgb(self.enemyTargetLabel, self.enemyTargetLabel.backgroundRole())
        config.data['spells']['target_text_color'] = get_rgb(self.enemyTargetLabel, self.enemyTargetLabel.foregroundRole())

        config.triggers = self.triggerTree.get_values()
        config.save()

    def set_values(self):
        for section, references in self._ref.items():
            for setting, widget in references.items():
                wt = type(widget)
                if wt == QCheckBox:
                    widget.setChecked(config.data[section][setting])
                elif wt == QSpinBox:
                    widget.setValue(config.data[section][setting])

        # set bar colors for spells
        # TODO: Finish setting up spells section

        # buff bar
        set_qcolor(
            self.buffBarLabel,
            foreground=config.data['spells']['buff_text_color'],
            background=config.data['spells']['buff_bar_color']
        )

        # debuff bar
        set_qcolor(
            self.debuffBarLabel,
            foreground=config.data['spells']['debuff_text_color'],
            background=config.data['spells']['debuff_bar_color']
        )

        # you target
        set_qcolor(
            self.youTargetLabel,
            foreground=config.data['spells']['target_text_color'],
            background=config.data['spells']['you_target_color']
        )

        # friendly target
        set_qcolor(
            self.friendlyTargetLabel,
            foreground=config.data['spells']['target_text_color'],
            background=config.data['spells']['friendly_target_color']
        )

        # enemey target
        set_qcolor(
            self.enemyTargetLabel,
            foreground=config.data['spells']['target_text_color'],
            background=config.data['spells']['enemy_target_color']
        )

        # Remove triggertree if it exists and reinsert it
        try:
            self.triggerTree.setParent(None)
        except:
            pass
        self.triggerTree = TriggerTree()
        self.triggerTree.edit_trigger.connect(self._edit_selected_trigger)
        self.treeViewLayout.insertWidget(0, self.triggerTree, 1)

    def _edit_selected_trigger(self):
        # if group, do nothing
        # if trigger, edit
        if not self.triggerTree.is_group_selected():
            try:
                item = self.triggerTree.selectedItems()[0]
                te = TriggerEditor(item.text(0), item.value)
                r = te.exec()
                if r:
                    updated = te.value()
                    if not self.triggerTree.trigger_exists(updated['name']):
                        item.setText(0, updated['name'])
                    item.value = updated['data']
                    item.setCheckState(
                        0,
                        Qt.Checked if updated['data']['__enabled__'] else Qt.Unchecked
                    )
            except IndexError:
                pass

    def _build_ref(self):
        d = {
            'general': {
                'update_check': self.updateCheckCheckBox,
                'parser_opacity': self.parserOpacitySpinBox,
                'qt_scale_factor': self.qTScalingSpinBox,
            },
            'maps': {
                'line_width': self.mapLineSizeSpinBox,
                'grid_line_width': self.gridLineSizeSpinBox,
                'current_z_alpha': self.currentLevelSpinBox,
                'closest_z_alpha': self.closestLevelSpinBox,
                'other_z_alpha': self.otherLevelsSpinBox
            },
            'spells': {
                'use_casting_window': self.useCastingWindowCheckBox,
                'casting_window_buffer': self.castingWindowTimeSpinBox,
                'use_secondary_all': self.usePVPSpellDurationsCheckBox
            }
        }
        return d