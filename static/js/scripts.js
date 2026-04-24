document.addEventListener('DOMContentLoaded', function () {
    var panels = document.querySelectorAll('[data-inline-panel]');

    function clearPanelInputs(panel) {
        var inputs = panel.querySelectorAll('input, textarea');
        inputs.forEach(function (input) {
            input.value = '';
        });
    }

    function syncPanelState(key, isOpen, resetValues) {
        var panel = document.querySelector('[data-inline-panel="' + key + '"]');
        var toggle = document.querySelector('[data-inline-toggle="' + key + '"]');

        if (!panel || !toggle) {
            return;
        }

        panel.classList.toggle('is-open', isOpen);
        toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        toggle.textContent = isOpen ? '-' : '+';

        if (!isOpen && resetValues) {
            clearPanelInputs(panel);
        }
    }

    panels.forEach(function (panel) {
        var key = panel.getAttribute('data-inline-panel');
        var toggle = document.querySelector('[data-inline-toggle="' + key + '"]');
        var closeButton = panel.querySelector('[data-inline-close="' + key + '"]');
        var startsOpen = panel.getAttribute('data-open') === 'true';

        syncPanelState(key, startsOpen, false);

        if (toggle) {
            toggle.addEventListener('click', function () {
                var isOpen = panel.classList.contains('is-open');
                syncPanelState(key, !isOpen, false);
            });
        }

        if (closeButton) {
            closeButton.addEventListener('click', function () {
                syncPanelState(key, false, true);
            });
        }
    });

    function initNominaSalaryDefaults() {
        var empleadoField = document.getElementById('id_empleado');
        var salarioField = document.getElementById('id_salario_base');
        var mapScript = document.getElementById('empleado-sueldo-map');

        if (!empleadoField || !salarioField || !mapScript) {
            return;
        }

        var sueldoMap = {};
        try {
            sueldoMap = JSON.parse(mapScript.textContent || '{}');
        } catch (error) {
            return;
        }

        function applyDefault(force) {
            var empleadoId = (empleadoField.value || '').trim();
            var sueldo = sueldoMap[empleadoId];

            if (sueldo === undefined) {
                return;
            }

            if (force || !(salarioField.value || '').trim()) {
                salarioField.value = sueldo;
            }
        }

        applyDefault(false);

        empleadoField.addEventListener('change', function () {
            applyDefault(true);
        });
    }

    initNominaSalaryDefaults();
});
