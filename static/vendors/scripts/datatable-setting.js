

$('document').ready(function () {
	$('.data-table').DataTable({
		destroy: true,
		scrollCollapse: true,
		autoWidth: false,
		serverSide: true,
		processing: false,
		ajax: {
			url: API_DATA_LIST_URL,
			type: 'GET',
			contentType: 'application/json',
			dataType: 'json',
			dataSrc: function (json) {
				for (var i = 0, ien = json.data.length; i < ien; i++) {
					let id = json.data[i][0]; // Captura o ID do item
					let urlUpdate = `${id}/update`
					json.data[i].push(
						'<div class="dropdown show">' +
						'<a class="btn btn-link font-24 p-0 line-height-1 no-arrow dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-expanded="true">' +
						'<i class="dw dw-more"></i>' +
						'</a>' +
						'<div class="dropdown-menu dropdown-menu-right dropdown-menu-icon-list">' +
						'<a class="dropdown-item view-item" data-toggle="modal" data-target="#modal-view" href="#" data-id="' + id + '"><i class="dw dw-eye"></i> View</a>' +
						'<a class="dropdown-item" href=' + urlUpdate + '><i class="dw dw-edit2"></i> Edit</a>' +
						'<a class="dropdown-item delete-item" href="#" data-id="' + id + '"><i class="dw dw-delete-3"></i> Delete</a>' +
						'</div>' +
						'</div>'
					);
				}
				return json.data;
			},

		},

		responsive: true,
		columnDefs: [{
			targets: "datatable-nosort",
			orderable: false,
		}],
		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, 500]],
		"language": {
			url: 'https://cdn.datatables.net/plug-ins/2.1.4/i18n/pt-BR.json',
		},
	});

	$('.data-table-export').DataTable({
		scrollCollapse: true,
		autoWidth: false,
		responsive: true,
		columnDefs: [{
			targets: "datatable-nosort",
			orderable: false,
		}],
		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
		"language": {
			"info": "_START_-_END_ of _TOTAL_ entries",
			searchPlaceholder: "Search",
			paginate: {
				next: '<i class="ion-chevron-right"></i>',
				previous: '<i class="ion-chevron-left"></i>'
			}
		},
		dom: 'Bfrtp',
		buttons: [
			'copy', 'csv', 'pdf', 'print'
		]
	});

	var table = $('.select-row').DataTable();
	$('.select-row tbody').on('click', 'tr', function () {
		if ($(this).hasClass('selected')) {
			$(this).removeClass('selected');
		}
		else {
			table.$('tr.selected').removeClass('selected');
			$(this).addClass('selected');
		}
	});

	var multipletable = $('.multiple-select-row').DataTable();
	$('.multiple-select-row tbody').on('click', 'tr', function () {
		$(this).toggleClass('selected');
	});
	var table = $('.checkbox-datatable').DataTable({
		'scrollCollapse': true,
		'autoWidth': false,
		'responsive': true,
		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
		"language": {
			"info": "_START_-_END_ of _TOTAL_ entries",
			searchPlaceholder: "Search",
			paginate: {
				next: '<i class="ion-chevron-right"></i>',
				previous: '<i class="ion-chevron-left"></i>'
			}
		},
		'columnDefs': [{
			'targets': 0,
			'searchable': false,
			'orderable': false,
			'className': 'dt-body-center',
			'render': function (data, type, full, meta) {
				return '<div class="dt-checkbox"><input type="checkbox" name="id[]" value="' + $('<div/>').text(data).html() + '"><span class="dt-checkbox-label"></span></div>';
			}
		}],
		'order': [[1, 'asc']]
	});

	$('#example-select-all').on('click', function () {
		var rows = table.rows({ 'search': 'applied' }).nodes();
		$('input[type="checkbox"]', rows).prop('checked', this.checked);
	});

	$('.checkbox-datatable tbody').on('change', 'input[type="checkbox"]', function () {
		if (!this.checked) {
			var el = $('#example-select-all').get(0);
			if (el && el.checked && ('indeterminate' in el)) {
				el.indeterminate = true;
			}
		}
	});
});

$(document).on('click', '.delete-item', function (e) {
	e.preventDefault(); // Impede que o link seja seguido

	let itemId = $(this).data('id'); // Pega o ID do item
	// Exibe uma confirmação utilizando SweetAlert
	Swal.fire({
		title: 'Tem certeza?',
		text: "Você não poderá reverter isso!",
		icon: 'warning',
		showCancelButton: true,
		confirmButtonColor: '#3085d6',
		cancelButtonColor: '#d33',
		confirmButtonText: 'Sim, deletar!',
		cancelButtonText: 'Cancelar'
	}).then((result) => {
		if (result.isConfirmed) {
			// Realiza a operação de delete via AJAX ou outra lógica de deleção
			const crsf = getCookie('csrftoken');
			$.ajax({
				url: '/api/users/?user_id=' + itemId, // Substitua com a URL correta
				type: 'DELETE',
				headers: {
					'X-CSRFToken': crsf
				},
				success: function (result) {
					Swal.fire({
						title: 'Deletado!',
						text: 'O item foi deletado com sucesso.',
						icon: 'success'
					}).then((result) => {
						if (result.isConfirmed) {
							// Recarrega a página
							window.location.reload();
						}
					});

				},
				error: function (xhr, status, error) {
					Swal.fire(
						'Erro!',
						'Ocorreu um erro ao deletar o item.',
						'error'
					);
				}
			});
		}
	});
});
